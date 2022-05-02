from typing import Optional, Dict
from pydantic.main import BaseModel

from hive.hardware_control.hw_entities import HardwareUrl


class PositionCoordinates(BaseModel):
    z: Optional[float]
    theta: Optional[float]


class ErdHardwareRoute(BaseModel):
    mdrive_z: HardwareUrl
    mdrive_theta: HardwareUrl
    mpa3: HardwareUrl


class ErdData(BaseModel):
    mdrive_z: Dict
    mdrive_theta: Dict
    mpa3: Dict
