from typing import Optional, Dict, Literal

from pydantic import Field
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


class ErdResult(BaseModel):
    erd_data: ErdData
    title: str



class ErdRecipe(BaseModel):
    measuring_time_sec: int
    type: Literal["erd"] = "erd"
    sample: str
    name: str
    theta: float
    z_start: float
    z_end: float
    z_increment: float
    z_repeat: int = Field(1, description="The recipe will run from z_start to z_end, for z_repeat times.")

