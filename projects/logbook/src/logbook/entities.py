from typing import List, Tuple

from pydantic import BaseModel
from datetime import datetime
from enum import Enum


class RbsRecipeType(Enum):
    STEPWISE_LEAST = "stepwise_least"
    STEPWISE = "stepwise"
    SINGLE_STEP = "single_step"


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


class RbsRecipeModel(BaseModel):
    type: RbsRecipeType
    sample: str
    recipe: str
    start_time: datetime
    end_time: datetime


class RbsSingleStepRecipe(RbsRecipeModel):
    type = RbsRecipeType.STEPWISE
    axis: str
    position: float


class RbsStepwiseRecipe(RbsRecipeModel):
    type = RbsRecipeType.STEPWISE
    vary_axis: str
    start: float
    end: float
    step: float


class RbsStepwiseLeastRecipe(RbsStepwiseRecipe):
    type = RbsRecipeType.STEPWISE_LEAST
    yield_positions: List[Tuple[float, int]]
    least_yield_position: float



