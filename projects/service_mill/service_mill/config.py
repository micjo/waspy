from typing import Optional

from pydantic import BaseSettings, BaseModel

from erd_entities import ErdConfig
from hw_entities import AnyConfig
from rbs_entities import RbsConfig
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
    TREND_STORE = "/root/trends/"
    LOGBOOK_URL = ""


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
