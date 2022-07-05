from datetime import timedelta
from pathlib import Path
from enum import Enum
from typing import List, Optional, Union, Literal, Annotated

from pydantic import Field, validator
from pydantic.generics import BaseModel

from hive.entities import SimpleConfig, AmlConfig, CaenConfig
from waspy.hardware_control.rbs_entities import CaenDetector, PositionCoordinates


class RbsHardware(BaseModel):
    aml_x_y: AmlConfig
    aml_phi_zeta: AmlConfig
    aml_det_theta: AmlConfig
    caen: CaenConfig
    motrona_charge: SimpleConfig


class RbsConfig(BaseModel):
    local_dir: Path
    remote_dir: Path
    hardware: RbsHardware


class CoordinateEnum(str, Enum):
    zeta = "zeta"
    theta = "theta"
    phi = "phi"


class VaryCoordinate(BaseModel):
    name: CoordinateEnum
    start: float
    end: float
    increment: float

    class Config:
        use_enum_values = True

    @validator('increment')
    def increment_must_be_positive_and_non_zero(cls, increment):
        if not increment >= 0:
            raise ValueError('increment must be positive')
        return increment

    @validator('end')
    def start_must_be_smaller_than_end(cls, end, values):
        if 'start' not in values:
            return
        if not values['start'] <= end:
            raise ValueError('end must be larger than or equal to start')
        return end


class Window(BaseModel):
    start: int
    end: int

    @validator('start', allow_reuse=True)
    def start_larger_than_zero(cls, start):
        if not start >= 0:
            raise ValueError('start must be positive')
        return start

    @validator('end', allow_reuse=True)
    def end_larger_than_zero(cls, end):
        if not end >= 0:
            raise ValueError('end must be positive')
        return end

    @validator('end', allow_reuse=True)
    def start_must_be_smaller_than_end(cls, end, values):
        if 'start' not in values:
            return
        if not values['start'] < end:
            raise ValueError("end must be larger then start")
        return end


class RecipeType(str, Enum):
    CHANNELING = "rbs_channeling"
    STEPWISE = "rbs_stepwise"
    STEPWISE_LEAST = "rbs_stepwise_least"
    SINGLE_STEP = "rbs_single_step"


class PositionModel(BaseModel):
    x: int
    y: int
    phi: int
    zeta: int
    det: int
    theta: int


class PauseModel(BaseModel):
    pause_dir_scan: bool


class StatusModel(str, Enum):
    Idle = "Idle"
    Running = "Running"


class RbsChanneling(BaseModel):
    """
    The model for a channeling measurement. This is a combination of recipes. A number of yield optimizations will
    happen. Next, a random measurement and a fixed measurement are performed.
    The outputs of the configured detectors are then compared in a plot.
    """
    type: Literal[RecipeType.CHANNELING]
    sample: str
    name: str
    start_position: Optional[PositionCoordinates]
    yield_charge_total: int
    yield_vary_coordinates: List[VaryCoordinate]
    yield_integration_window: Window
    yield_optimize_detector_identifier: str
    random_fixed_charge_total: int
    random_vary_coordinate: VaryCoordinate

    class Config:
        extra = 'forbid'


class RbsStepwiseLeast(BaseModel):
    """ The model for a yield minimization run. The sample will be moved along the vary_coordinate axis. For each step,
    the energy yield is calculated by integrating the histogram. Then the yields are fitted and the sample will be moved
    to the position with minimum yield """
    type: Literal[RecipeType.STEPWISE_LEAST]
    sample: str
    name: str
    start_position: Optional[PositionCoordinates]
    total_charge: int
    vary_coordinate: VaryCoordinate
    integration_window: Window
    optimize_detector_identifier: str


class RbsStepwise(BaseModel):
    """ The model for a stepwise (a.k.a. random) measurement - the vary_coordinate will be changed"""
    type: Literal[RecipeType.STEPWISE]
    sample: str
    name: str
    start_position: Optional[PositionCoordinates]
    charge_total: int
    vary_coordinate: VaryCoordinate


class RbsSingleStep(BaseModel):
    """ The model for a fixed measurement - all coordinates are kept the same"""
    type: Literal[RecipeType.SINGLE_STEP]
    sample: str
    name: str
    charge_total: int


class RbsJobModel(BaseModel):
    recipes: List[Annotated[Union[RbsChanneling, RbsStepwise], Field(discriminator='type')]]
    name: str
    type = "rbs"

    class Config:
        use_enum_values = True

        schema_extra = {
            'example':
                {
                    "name": "RBS21_071", "type": "rbs",
                    "recipes": [
                        {"type": "rbs_stepwise", "sample": "AE007607_D02_A", "name": "RBS21_071_01B_A",
                         "start_position": {"x": 10, "y": 22, "phi": 0}, "charge_total": 45000,
                         "vary_coordinate": {"name": "phi", "start": 0, "end": 30, "increment": 2}
                         },
                        {"type": "rbs_stepwise", "sample": "AE007607_D02_B", "name": "RBS21_071_08B_A",
                         "start_position": {"x": 10, "y": 22, "phi": 0}, "charge_total": 45000,
                         "vary_coordinate": {"name": "phi", "start": 0, "end": 30, "increment": 2}
                         },
                        {
                            "type": "rbs_channeling", "sample": "AE007607_D02_A", "name": "RBS21_071_01B_A",
                            "start_position": {"x": 10, "y": 22, "phi": 0}, "yield_charge_total": 2100,
                            "yield_vary_coordinates": [
                                {"name": "zeta", "start": -2, "end": 2, "increment": 0.2},
                                {"name": "theta", "start": -2, "end": 2, "increment": 0.2},
                                {"name": "zeta", "start": -2, "end": 2, "increment": 0.2},
                                {"name": "theta", "start": -2, "end": 2, "increment": 0.2}
                            ],
                            "yield_integration_window": {"start": 22, "end": 53},
                            "yield_optimize_detector_index": 0,
                            "random_fixed_charge_total": 1000,
                            "random_vary_coordinate": {"name": "phi", "start": 0, "end": 30, "increment": 2}
                        }
                    ]
                }
        }


empty_rbs_job = RbsJobModel(recipes=[], name="", detectors=[])


class ActiveRecipe(BaseModel):
    recipe_id: str
    run_time: timedelta
    accumulated_charge_corrected: float
    accumulated_charge_target: float


class RbsRqmStatus(BaseModel):
    run_status: StatusModel
    active_rqm_status: List[ActiveRecipe]


empty_rqm_status = RbsRqmStatus(run_status=StatusModel.Idle, active_rqm_status=[])


class ExperimentStateModel(BaseModel):
    status: StatusModel
    experiment: RbsJobModel

    class Config:
        use_enum_values = True
