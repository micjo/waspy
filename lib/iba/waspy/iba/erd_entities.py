from datetime import datetime
from typing import Optional, Dict, Literal

from pydantic import Field
from pydantic.main import BaseModel


class PositionCoordinates(BaseModel):
    z: Optional[float]
    theta: Optional[float]


class ErdDriverUrls(BaseModel):
    mdrive_z: str
    mdrive_theta: str
    mpa3: str
    motrona_z_encoder: str
    motrona_theta_encoder: str


class ErdData(BaseModel):
    mdrive_z: Dict
    mdrive_theta: Dict
    mpa3: Dict
    motrona_z_encoder: Dict
    motrona_theta_encoder: Dict
    histogram: str
    measuring_time_sec: float
    mpa3_workaround_trigger: bool


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


class ErdJournal(BaseModel):
    start_time: datetime
    end_time: datetime
    measuring_time_sec: int
    z: float
    theta: float
    z_encoder: float
    theta_encoder: float
    histogram: str
    extended_flt_data: list[list[float]]
    mpa3_workaround_trigger: bool

def get_erd_journal(erd_data: ErdData, start_time: datetime, extended_flt_data: list[list[float]]) -> ErdJournal:
    return ErdJournal(
        start_time=start_time, end_time=datetime.now(), measuring_time_sec=erd_data.measuring_time_sec,
        z=erd_data.mdrive_z["motor_position"], theta=erd_data.mdrive_theta["motor_position"],
        z_encoder=erd_data.motrona_z_encoder["charge(nC)"],
        theta_encoder=erd_data.motrona_theta_encoder["charge(nC)"],
        histogram=erd_data.histogram, 
        mpa3_workaround_trigger = erd_data.mpa3_workaround_trigger,
        extended_flt_data = extended_flt_data)
