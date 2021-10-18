from pathlib import Path
from typing import Optional

from pydantic import BaseSettings, BaseModel

from app.hardware_controllers.entities import HwControllerConfig
import logging
import tomli

logging.basicConfig(
    format='[%(asctime)s.%(msecs)03d] [%(levelname)s] %(message)s',
    level=logging.INFO,
    datefmt='%Y.%m.%d__%H:%M__%S')


class InputDirConfig(BaseModel):
    watch: Path


class OutputDirConfig(BaseModel):
    ongoing: Path
    done: Path
    failed: Path
    data: Path


class HiveConfig(BaseModel):
    daemonConfig: HwControllerConfig
    input_dir: InputDirConfig
    output_dir: OutputDirConfig
    output_dir_remote: OutputDirConfig


EMPTY_INPUT_DIR = InputDirConfig(watch="./input")
EMPTY_OUTPUT_DIR = OutputDirConfig(ongoing=".", done=".", failed=".", data=".")
EMPTY_DAEMON_CONFIG = HwControllerConfig(daemons=[])


class GlobalConfig(BaseSettings):
    CONFIG_FILE: Optional[str]
    FAKER = False
    ENV_STATE = "dev"


class MakeHiveConfig:
    def __init__(self, config_file: Optional[str]):
        self.config_file = config_file

    def __call__(self):
        if self.config_file:
            with open(self.config_file, "rb") as f:
                conf_from_file = tomli.load(f)
                daemons = HwControllerConfig.parse_obj(conf_from_file)
                input_dir = InputDirConfig.parse_obj(conf_from_file['rbs']['input_dir'])
                output_dir = OutputDirConfig.parse_obj(conf_from_file['rbs']['output_dir'])
                output_dir_remote = OutputDirConfig.parse_obj(conf_from_file['rbs']['remote_output_dir'])
                return HiveConfig(daemonConfig=daemons, input_dir=input_dir, output_dir=output_dir,
                                  output_dir_remote=output_dir_remote)

        else:
            return HiveConfig(daemonConfig=EMPTY_DAEMON_CONFIG, input_dir=EMPTY_INPUT_DIR, output_dir=EMPTY_OUTPUT_DIR,
                              output_dir_remote=EMPTY_OUTPUT_DIR)


env_conf = GlobalConfig()
logging.info("Loaded config: " + env_conf.json())
cfg = MakeHiveConfig(env_conf.CONFIG_FILE)()
logging.info("Parsed config: " + cfg.json())


