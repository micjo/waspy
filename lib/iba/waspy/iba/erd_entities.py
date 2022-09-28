from typing import Optional, Dict
from pydantic.main import BaseModel


class PositionCoordinates(BaseModel):
    z: Optional[float]
    theta: Optional[float]


class HardwareUrl(BaseModel):
    url: str


class ErdDriverUrls(BaseModel):
    mdrive_z: HardwareUrl
    mdrive_theta: HardwareUrl
    mpa3: HardwareUrl


class ErdData(BaseModel):
    mdrive_z: Dict
    mdrive_theta: Dict
    mpa3: Dict
    histogram: str
    measuring_time_sec: float
