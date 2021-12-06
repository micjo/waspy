from pathlib import Path
from typing import Optional, Dict

from pydantic import BaseSettings, BaseModel

from app.erd.entities import ErdConfig
from app.hardware_controllers.entities import AnyConfig
from app.rbs.entities import RbsConfig
import logging
import tomli

logging.basicConfig(
    format='[%(asctime)s.%(msecs)03d] [%(levelname)s] %(message)s',
    level=logging.INFO,
    datefmt='%Y.%m.%d__%H:%M__%S')


class HiveConfig(BaseModel):
    any: AnyConfig
    rbs: RbsConfig
    erd: ErdConfig


class GlobalConfig(BaseSettings):
    CONFIG_FILE: Optional[str]
    FAKER = False
    ENV_STATE = "dev"


def make_hive_config(config_file) -> HiveConfig:
    with open(config_file, "rb") as f:
        conf_from_file = tomli.load(f)
        print(conf_from_file)

        for setup_key, setup_item in conf_from_file.items():
            print(setup_key)
            for hardware_key, hardware_item in setup_item["hardware"].items():
                hardware_item["proxy"] = "/api/" + setup_key + "/" + hardware_key
                print(hardware_item)

        return HiveConfig.parse_obj(conf_from_file)
