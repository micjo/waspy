from typing import List, Tuple, Annotated, Union, Literal, Optional

from pydantic import BaseModel, Field
from datetime import datetime
from enum import Enum


class RbsRecipeType(str, Enum):
    ANGULAR_YIELD = "rbs_angular_yield"
    RANDOM = "rbs_random"
    FIXED = "rbs_fixed"


class ErdRecipeModel(BaseModel):
    type: Literal["erd"] = "erd"
    sample: str
    name: str
    measuring_time_sec: int
    theta: float
    z_start: float
    z_end: float
    z_increment: float
    z_repeat: int
    start_time: datetime
    end_time: datetime
    average_terminal_voltage: float


class ToolStatus(BaseModel):
    area: str
    beam_description: str
    beam_energy_MeV: float
    snics_cathode_target: str
    bias_voltage_kV: float
    bias_current_mA: float
    focus_voltage_kV: float
    focus_current_mA: float
    oven_power_percentage: int
    over_temperature_celsius: int
    ionizer_current_A: float
    ionizer_voltage_V: float
    cathode_probe_voltage_kV: float
    cathode_probe_current_mA: float


class RbsRecipeModel(BaseModel):
    type: RbsRecipeType
    sample: str
    name: str
    start_time: datetime
    end_time: datetime


class RbsSingleStepRecipe(RbsRecipeModel):
    type: Literal[RbsRecipeType.FIXED] = RbsRecipeType.FIXED


class RbsStepwiseRecipe(RbsRecipeModel):
    type: Literal[RbsRecipeType.RANDOM] = RbsRecipeType.RANDOM
    vary_axis: str
    start: float
    end: float
    step: float


class RbsStepwiseLeastRecipe(RbsStepwiseRecipe):
    type: Literal[RbsRecipeType.ANGULAR_YIELD] = RbsRecipeType.ANGULAR_YIELD
    yield_positions: List[Tuple[float, int]]
    least_yield_position: float


class Accelerator(BaseModel):
    area: Optional[str]
    beam_description: Optional[str]
    beam_energy_MeV: Optional[float]
    snics_cathode_target: Optional[str]
    bias_voltage_kV: Optional[float]
    bias_current_mA: Optional[float]
    focus_voltage_kV: Optional[float]
    focus_current_mA: Optional[float]
    oven_power_percentage: Optional[int]
    oven_temperature_celsius: Optional[int]
    ionizer_current_A: Optional[float]
    ionizer_voltage_V: Optional[float]
    cathode_probe_voltage_kV: Optional[float]
    cathode_probe_current_mA: Optional[float]



class AnyRecipe(BaseModel):
    __root__: Union[RbsStepwiseRecipe, RbsSingleStepRecipe, RbsStepwiseLeastRecipe, ErdRecipeModel] = \
        Field(..., discriminator='type')
