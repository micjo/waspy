from typing import List

from pydantic.generics import BaseModel
from pathlib import Path
from enum import Enum


class DaemonType(str, Enum):
    aml = 'aml'
    motrona = 'motrona'
    caen = 'caen'


class AmlConfig(BaseModel):
    type: DaemonType
    title: str
    url: str
    names: List[str]
    loads: List[float]

    class Config:
        use_enum_values = True


class SimpleConfig(BaseModel):
    type: DaemonType
    title: str
    url: str

    class Config:
        use_enum_values = True


class DaemonConfig(BaseModel):
    aml_x_y: AmlConfig
    aml_phi_zeta: AmlConfig
    aml_det_theta: AmlConfig
    motrona_rbs: SimpleConfig
    caen_rbs: SimpleConfig

    class Config:
        use_enum_values = True


class InputDirConfig(BaseModel):
    watch: Path


class OutputDirConfig(BaseModel):
    ongoing: Path
    done: Path
    failed: Path
    data: Path


class HiveConfig(BaseModel):
    daemons: DaemonConfig
    input_dir: InputDirConfig
    output_dir: OutputDirConfig
    output_dir_remote: OutputDirConfig


EMPTY_DAEMON_CONFIG = DaemonConfig(
    aml_x_y=AmlConfig(type="aml", title="aml_1", url="url_1", names=["a", "b"], loads=[0, 0]),
    aml_phi_zeta=AmlConfig(type="aml", title="aml_2", url="url_2", names=["a", "b"], loads=[0, 0]),
    aml_det_theta=AmlConfig(type="aml", title="aml_3", url="url_3", names=["a", "b"], loads=[0, 0]),
    motrona_rbs=SimpleConfig(type="motrona", title="motrona_1", url="url_4"),
    caen_rbs=SimpleConfig(type="caen", title="caen_1", url="url_5")
)

EMPTY_INPUT_DIR = InputDirConfig(watch="./input")
EMPTY_OUTPUT_DIR = OutputDirConfig(ongoing=".", done=".", failed=".", data=".")
