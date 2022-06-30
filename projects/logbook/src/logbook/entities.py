from typing import List, Tuple, Annotated, Union, Literal

from pydantic import BaseModel, Field
from datetime import datetime
from enum import Enum


class RbsRecipeType(str, Enum):
    STEPWISE_LEAST = "rbs_stepwise_least"
    STEPWISE = "rbs_stepwise"
    SINGLE_STEP = "rbs_single_step"


class ErdRecipeModel(BaseModel):
    type = "erd"
    beam_type: str
    beam_energy_MeV: float
    sample_tilt_degrees: float
    sample: str
    recipe: str
    measuring_time_sec: int
    theta: float
    z_start: float
    z_end: float
    z_increment: float
    z_repeat: int
    start_time: datetime
    end_time: datetime
    average_terminal_voltage: float


class RbsRecipeModel(BaseModel):
    type: RbsRecipeType
    sample: str
    recipe: str
    start_time: datetime
    end_time: datetime


class RbsSingleStepRecipe(RbsRecipeModel):
    type: Literal[RbsRecipeType.SINGLE_STEP] = RbsRecipeType.SINGLE_STEP
    axis: str
    position: float


class RbsStepwiseRecipe(RbsRecipeModel):
    type: Literal[RbsRecipeType.STEPWISE] = RbsRecipeType.STEPWISE
    vary_axis: str
    start: float
    end: float
    step: float


class RbsStepwiseLeastRecipe(RbsStepwiseRecipe):
    type: Literal[RbsRecipeType.STEPWISE_LEAST] = RbsRecipeType.STEPWISE_LEAST
    yield_positions: List[Tuple[float, int]]
    least_yield_position: float


class AnyRbs(BaseModel):
    __root__: Union[RbsStepwiseRecipe, RbsSingleStepRecipe, RbsStepwiseLeastRecipe] = Field(..., discriminator='type')




