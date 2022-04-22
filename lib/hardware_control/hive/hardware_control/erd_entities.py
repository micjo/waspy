from typing import Optional
from pydantic.main import BaseModel

from hive.hardware_control.hw_entities import HardwareUrl


class PositionCoordinates(BaseModel):
    z: Optional[float]
    theta: Optional[float]


class ErdHardwareRoute(BaseModel):
    mdrive_z: HardwareUrl
    mdrive_theta: HardwareUrl
    mpa3: HardwareUrl

