from __future__ import annotations

import os
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import Dict, Optional

import pandas as pd

from mcal.config import MCalConfig, load_config_file
from mcal.samplers.base import SamplerData
from mcal.utils.logging import get_logger

# NOTE: I think it is important that %Z is included to assure UTC
DATE_FORMAT = "%Y-%m-%d_%H:%M:%S_%Z"

logger = get_logger(__name__)

# TODO: Unify with / include in CalibrationRun
@dataclass
class RunStats:
    time_elapsed: timedelta = timedelta(seconds=0)
    iterations: int = 0

    def get_str(self) -> str:
        return "\t" + "\n\t".join((
            f"Iterations: {self.iterations}",
            f"Time elapsed: {self.time_elapsed}",
        ))

@dataclass
class CalibrationRun:
    start_time: datetime
    config: MCalConfig
    collected_data: Dict[str, SamplerData] = field(default_factory=lambda: {})

    def gen_name(self) -> str:
        return self.start_time.strftime(DATE_FORMAT)

    def write_run(
        self,
        save_directory: Optional[str] = None,
        name: Optional[str] = None,
        data_type: str = 'csv'
    ) -> str:
        if save_directory is None:
            save_directory = 'mcal_run_data'
        if name is None:
            name = self.gen_name()

        folder_path = os.path.join(save_directory, name)
        if os.path.exists(folder_path):
            # TODO: Remove this, really bad to error if run has data
            raise RuntimeError("Write path already exists: %s", folder_path)

        os.makedirs(folder_path)
        logger.info("Writing sample run to directory: %s" % folder_path)

        config_path = os.path.join(folder_path, "config.yml")
        self.config.save(config_path)

        for sample in self.collected_data.values():
            sample.write(folder_path)

        return folder_path

def load_run(path: str) -> CalibrationRun:
    try:
        folder_name = os.path.basename(path)
        start_time = datetime.strptime(folder_name, DATE_FORMAT)
    except ValueError:
        start_time = None

    config = None
    collected_data = {}
    for file in os.listdir(path):
        file_path = os.path.join(path, file)
        if file == "config.yml":
            # NOTE: Config file should be fully rendered when saved
            config = load_config_file(file_path, {})
            continue

        name, ext = os.path.splitext(file)
        if ext == ".json":
            # Used for saving CSV dtypes so just skipping here
            continue
        if ext == ".csv":
            collected_data[name] = SamplerData.load(file_path)
        else:
            raise NotImplementedError("Found unexpected type in save folder: %s" % ext)

    if config is None:
        # TODO: Definitely can optimize this if data load times get larger
        raise RuntimeError("Unable to find 'config.yml' file in directory: %s" % path)
    if len(collected_data) == 0:
        logger.warning("Not sample data was found in directory, returning a sample run with empty data: %s" % path)

    return CalibrationRun(
        start_time=start_time,
        config=config,
        collected_data=collected_data
    )