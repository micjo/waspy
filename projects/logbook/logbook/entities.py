from pydantic import BaseModel
from datetime import datetime


class ErdRecipeModel(BaseModel):
    job_id: str
    type = "erd"
    beam_type: str
    beam_energy_MeV: float
    sample_tilt_degrees: float
    sample_id: str
    file_stem: str
    measuring_time_sec: int
    theta: float
    z_start: float
    z_end: float
    z_increment: float
    z_repeat: int
    start_time: datetime
    end_time: datetime
    avg_terminal_voltage: float
