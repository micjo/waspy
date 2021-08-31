import os
from typing import Optional

from pydantic import BaseSettings

from app.setup.entities import DaemonConfig, OutputDirConfig, InputDirConfig, EMPTY_DAEMON_CONFIG, \
    HiveConfig, EMPTY_INPUT_DIR, EMPTY_OUTPUT_DIR
import logging
import tomli

logging.basicConfig(
    format='[%(asctime)s.%(msecs)03d] [%(levelname)s] %(message)s',
    level=logging.INFO,
    datefmt='%Y.%m.%d__%H:%M__%S')


class GlobalConfig(BaseSettings):
    CONFIG_FILE: Optional[str]
    FAKER = False
    ENV_STATE: str


class MakeHiveConfig:
    def __init__(self, config_file: Optional[str]):
        self.config_file = config_file

    def __call__(self):
        if self.config_file:
            with open(self.config_file, "rb") as f:
                conf_from_file = tomli.load(f)
                daemons = DaemonConfig.parse_obj(conf_from_file["hw_control"])
                input_dir = InputDirConfig.parse_obj(conf_from_file['rbs']['input_dir'])
                output_dir = OutputDirConfig.parse_obj(conf_from_file['rbs']['output_dir'])
                output_dir_remote = OutputDirConfig.parse_obj(conf_from_file['rbs']['remote_output_dir'])
                return HiveConfig(daemons=daemons, input_dir=input_dir, output_dir=output_dir,
                                  output_dir_remote=output_dir_remote)

        else:
            return HiveConfig(daemons=EMPTY_DAEMON_CONFIG, input_dir=EMPTY_INPUT_DIR, output_dir=EMPTY_OUTPUT_DIR,
                              output_dir_remote=EMPTY_OUTPUT_DIR)


env_conf = GlobalConfig()
logging.info("Loaded config: " + str(env_conf))
cfg = MakeHiveConfig(env_conf.CONFIG_FILE)()
logging.info("Parsed config: " + str(cfg))
