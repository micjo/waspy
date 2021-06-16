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
    first_name: str
    second_name: str
    first_load: int
    second_load: int
    url: str

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
