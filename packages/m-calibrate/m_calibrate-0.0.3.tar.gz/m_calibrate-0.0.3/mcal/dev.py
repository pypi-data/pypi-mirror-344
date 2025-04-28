from __future__ import annotations

import os
import subprocess
import time
from abc import ABC, abstractmethod
from typing import List, Optional, Set
from uuid import uuid4

from pydantic import BaseModel, Field

from mcal.files import K8_NR_HELM_VALUES, load_to_temp_file
from mcal.utils.cmd import is_cmd, run_cmd
from mcal.utils.env_file import load_env_file
from mcal.utils.logging import get_logger
from mcal.utils.shared_model import SharedModel

logger = get_logger(__name__)

THIS_DIR = os.path.abspath(os.path.dirname(__file__))

class ClusterData(BaseModel):
    @staticmethod
    def data_path(name: str) -> str:
        return os.path.join(THIS_DIR, f"{name}.json")

    name: str
    users: int = Field(default=1)
    created_from: str
    labels: Set[str] = Field(default_factory=lambda: set())

    def config_path(self) -> str:
        # NOTE: Not sure if this is the best way of doing things
        return os.path.join(THIS_DIR, f"{self.name}-kubeconfig")

class DevCluster:
    def __init__(
        self,
        name: str,
        create: bool = False,
        release_on_del: bool = True,
        created_from: str = 'python',
        create_args: List[str] = None
    ):
        assert name.startswith('mcal-dev'), "Cluster names should start with 'mcal-dev-' prefix not: %s" % name

        self.name = name
        self.release_on_del = release_on_del


        if create:
            self._create(created_from, create_args)
        else:
            self.shared_data = SharedModel(ClusterData, ClusterData.data_path(self.name))
            with self.shared_data as d:
                d.users += 1

    def _create(self, created_from: str, create_args: List[str] = None):
        if not is_cmd('kind'):
            logger.error("Development cluster creation relies on 'kind' CLI being installed but none found.")

        if create_args is None:
            create_args = []

        data_path = ClusterData.data_path(self.name)
        assert not os.path.exists(data_path), "Cluster with same name already created: %s" % data_path

        data = ClusterData(
            name=self.name,
            created_from=created_from
        )

        kind_command = [
            'kind', 'create', 'cluster',
            '--name', self.name,
            '--kubeconfig', data.config_path(),
            *create_args
        ]
        logger.info("Using 'kind' to create cluster with name: %s" % self.name)
        run_cmd(
            kind_command,
        )

        # After cluster startup works, write shared data file to disk
        # TODO: Why do I need the extra type annotation here?
        self.shared_data: SharedModel[ClusterData] = SharedModel.initialize(data, data_path)

    def _delete(self, d: ClusterData = None):
        if d is None:
            # TODO: Cleaner way to do this?
            d = self.shared_data.__enter__()

        self.shared_data.mark_for_delete()
        run_cmd(
            [
                'kind', 'delete', 'cluster',
                '--name', self.name
            ]
        )

        self.shared_data.delete()
        os.remove(d.config_path())

    def __del__(self):
        if not hasattr(self, 'release_on_del'):
            # Early errors can cause this
            return
        if self.release_on_del:
            if not hasattr(self, 'shared_data'):
                # Early errors can cause this
                return

            if self.shared_data.deleted:
                return

            with self.shared_data as d:
                d.users -= 1

                if d.users == 0:
                    logger.warning("Shutting down cluster as no remaining users: %s" % d.name)

                    # Delete cluster!
                    self._delete(d)

def list_clusters() -> List[DevCluster]:
    clusters = os.listdir(THIS_DIR)
    clusters = filter(
        lambda name: name.startswith('mcal-dev-') and name.endswith('.json'),
        clusters
    )
    clusters = map(
        lambda name: DevCluster(name=name.removesuffix('.json')),
        clusters
    )

    return list(clusters)

def which_cluster() -> Optional[str]:
    config = os.environ.get('KUBECONFIG')
    if config is None:
        return None

    config_name = os.path.basename(config)
    if config_name.startswith('mcal-dev-') and config_name.endswith('-kubeconfig'):
        return config_name.removesuffix('-kubeconfig')

def get_cluster(cluster_name: Optional[str] = None) -> Optional[DevCluster]:
    clusters = list_clusters()
    if len(clusters) == 0:
        return None

    if cluster_name is not None:
        for cluster in clusters:
            if cluster.name == cluster_name:
                return cluster
        return None

    return clusters[0]

class Apply(ABC):
    @abstractmethod
    def apply(cluster_name: str, **kwargs) -> Optional[List[str]]:
        pass

class MetricsServer(Apply):
    def apply(self, cluster_name: str) -> List[str]:
        if not is_cmd('kubectl') or not is_cmd('helm'):
            raise RuntimeError("Cluster bootstrap requires both 'kubectl' and 'helm' to be installed")

        logger.info("Testing cluster connection")
        result = run_cmd(
            ['kubectl', 'cluster-info'],
            expected_return_codes=[0, 1] # Expecting 1 to handle gracefully
        )
        if result.returncode == 1:
            raise RuntimeError("Unable to get cluster info via 'kubectl', is the cluster active")

        logger.info("Adding NR helm repo")
        run_cmd(
            ['helm', 'repo', 'add', 'metrics-server', 'https://kubernetes-sigs.github.io/metrics-server/'],
        )

        run_cmd(
            ["helm", "upgrade", "--install", "metrics-server", "metrics-server/metrics-server", "--wait"]
        )

        return [
            'apply/metrics_server'
        ]

class NRI(Apply):
    def apply(self, cluster_name: str, env_file: str = None) -> List[str]:
        if env_file is not None:
            env = load_env_file(env_file)
        else:
            env = load_env_file()

        if not is_cmd('kubectl') or not is_cmd('helm'):
            raise RuntimeError("Cluster bootstrap requires both 'kubectl' and 'helm' to be installed")

        logger.info("Rendering helm values...")
        helm_values_path = load_to_temp_file(
            file=K8_NR_HELM_VALUES,
            arguments={
                'cluster_name': cluster_name,
                'license_key': env.get_license_key()
            }
        )

        logger.info("Testing cluster connection")
        result = run_cmd(
            ['kubectl', 'cluster-info'],
            expected_return_codes=[0, 1] # Expecting 1 to handle gracefully
        )
        if result.returncode == 1:
            raise RuntimeError("Unable to get cluster info via 'kubectl', is the cluster active")

        logger.info("Adding NR helm repo")
        run_cmd(
            ['helm', 'repo', 'add', 'newrelic', 'https://helm-charts.newrelic.com'],
        )

        helm_args = [
            'helm', 'upgrade', '--install', 'newrelic-bundle', 'newrelic/nri-bundle',
            # '--version', '3.37.3',
            '--namespace', 'newrelic', '--create-namespace',
            '-f', helm_values_path.name,
            '--wait',
            # Validating args
            '--dry-run',
            '--debug'
        ]
        logger.info("Validating helm command...")
        # with open(helm_values_path.name, 'r') as f:
        #     print(f.read())
        run_cmd(
            helm_args
        )


        logger.info("Bootstrapping activate kubetctl context with NR integration, naming cluster '%s'" % cluster_name)
        helm_args.remove('--dry-run')
        helm_args.remove('--debug')
        run_cmd(
            helm_args
        )

        logger.info("Bootstraping complete!")
        logger.info("Note: Services may take a while to spin up, check status with the command below.")
        print('\tkubectl -n newrelic get pods')
        # TODO: Preform monitoring here?

        return [
            'apply/new_relic'
        ]

class DaskOperator(Apply):
    def apply(self, cluster_name: str):
        if not is_cmd('kubectl') or not is_cmd('helm'):
            raise RuntimeError("Cluster bootstrap requires both 'kubectl' and 'helm' to be installed")

        logger.info("Testing cluster connection")
        result = run_cmd(
            ['kubectl', 'cluster-info'],
            expected_return_codes=[0, 1] # Expecting 1 to handle gracefully
        )
        if result.returncode == 1:
            raise RuntimeError("Unable to get cluster info via 'kubectl', is the cluster active")

        logger.info("Adding DaskOperator")
        run_cmd([
            'helm', 'install',
            '--repo', 'https://helm.dask.org',
            '--create-namespace', '-n', 'dask-operator',
            '--generate-name', 'dask-kubernetes-operator'
        ])

        return [
            'apply/dask_operator'
        ]

APPLIES = {
    'MetricsServer': MetricsServer,
    'NRI': NRI,
    'DaskOperator': DaskOperator,
}

class DummyMount:
    """Context manager for creating and managing a dummy pod with PVC."""
    
    def __init__(self, pvc_name: str, namespace: str = None):
        self.pvc_name = pvc_name
        self.pod_name = f"dummy-pod-{uuid4()}"
        self.namespace = namespace
        self._entered = False
        # Load and render the dummy pod manifest with the PVC name
        self._tmp_file = load_to_temp_file(
            'k8/manifest-dummy-pod.yml',
            arguments={
                'volume_name': self.pvc_name,
                'pod_name': self.pod_name,
                'namespace': self.namespace
            }
        )

    def _with_namespace(self, cmd: list) -> list:
        """Add namespace flag to command if namespace is specified."""
        if self.namespace:
            cmd.extend(['-n', self.namespace])
        return cmd

    def _namespace_info(self) -> str:
        """Get namespace info string for logging."""
        return f" in namespace {self.namespace}" if self.namespace else ""

    def _wait_for_pod_ready(self, timeout: int = 60) -> bool:
        """Wait for pod to be ready, with timeout."""
        start_time = time.time()
        while time.time() - start_time < timeout:
            cmd = self._with_namespace(['kubectl', 'get', 'pod', '--ignore-not-found', self.pod_name, '-o', 'jsonpath="{.status.phase}"'])
            result = run_cmd(
                args=cmd,
                stdout=subprocess.PIPE
            )
            if result.stdout.decode().strip() == '"Running"':
                return True
            time.sleep(1)
        return False

    def __enter__(self) -> DummyMount:
        """Create the dummy pod and wait for it to be ready."""
        if self._entered:
            raise RuntimeError("DummyMount context manager cannot be entered twice")
        self._entered = True

        # Apply the manifest
        try:
            run_cmd(
                args=['kubectl', 'apply', '-f', self._tmp_file.name],
                stdout=subprocess.PIPE
            )
        except:
            logger.error("Failed to apply manifest:")
            logger.error("---")
            with open(self._tmp_file.name) as f:
                for line in f:
                    logger.error(line.rstrip())
            logger.error("---")
            raise

        logger.info(f"Creating dummy pod {self.pod_name}{self._namespace_info()} with PVC {self.pvc_name}...")

        # Wait for pod to be ready
        if not self._wait_for_pod_ready():
            self.__exit__(None, None, None)  # Cleanup on failure
            raise RuntimeError(f"Pod {self.pod_name} failed to start within timeout")

        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Clean up the dummy pod."""
        try:
            cmd = self._with_namespace(['kubectl', 'delete', 'pod', self.pod_name, '--ignore-not-found'])
            run_cmd(
                args=cmd,
                stdout=subprocess.PIPE
            )
            logger.info(f"Deleted dummy pod {self.pod_name}{self._namespace_info()}")
        except subprocess.CalledProcessError as e:
            logger.error(f"Failed to delete pod {self.pod_name}: {e}")
        finally:
            if self._tmp_file:
                self._tmp_file.close()