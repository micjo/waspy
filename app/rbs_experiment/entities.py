from enum import Enum
from typing import List, Optional, Union, Literal

from pydantic import Field, validator, root_validator
from pydantic.generics import BaseModel

from app.hardware_controllers.entities import AmlConfig, SimpleConfig


class RbsConfig(BaseModel):
    aml_x_y: AmlConfig
    aml_phi_zeta: AmlConfig
    aml_det_theta: AmlConfig
    caen: SimpleConfig
    motrona: SimpleConfig


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


class PositionCoordinates(BaseModel):
    x: Optional[float]
    y: Optional[float]
    phi: Optional[float]
    zeta: Optional[float]
    detector: Optional[float]
    theta: Optional[float]

    def __str__(self):
        return "position_{x}_{y}_{phi}_{zeta}_{det}_{theta}".format(x=self.x, y=self.y, phi=self.phi, zeta=self.zeta,
                                                                    det=self.detector, theta=self.theta)


class CoordinateEnum(str, Enum):
    zeta = "zeta"
    theta = "theta"
    phi = "phi"


class RecipeType(str, Enum):
    channeling = "channeling"
    random = "random"
    minimize_yield = "minimize_yield"
    fixed = "fixed"


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


class CaenDetectorModel(BaseModel):
    board: int
    channel: int
    identifier: str = Field(
        description="This will be used in the filenames for storage and in the plots for titles")
    bins_min: int
    bins_max: int
    bins_width: int = Field(
        description="The range between min and max will be rescaled to this value, The bins are combined with integer sized bin intervals. values on the maximum side are potentially discared")


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


class HistogramMetaData(BaseModel):
    file_stem: str
    sample_id: str
    detector_id: str
    measuring_time_msec: str
    charge: str
    x: float
    y: float
    phi: float
    zeta: float
    det: float
    theta: float


class RbsRqmChanneling(BaseModel):
    """
    The model for a channeling measurement. This is a combination of recipes. A number of yield optimizations will
    happen. Next, a random measurement and a fixed measurement are performed.
    The outputs of the configured detectors are then compared in a plot.
    """
    type: Literal[RecipeType.channeling]
    sample_id: str
    file_stem: str
    start_position: Optional[PositionCoordinates]
    yield_charge_total: int
    yield_vary_coordinates: List[VaryCoordinate]
    yield_integration_window: Window
    yield_optimize_detector_index: int
    random_fixed_charge_total: int
    random_vary_coordinate: VaryCoordinate

    class Config:
        extra = 'forbid'


class RbsRqmMinimizeYield(BaseModel):
    """ The model for a yield minimization run. The sample will be moved along the vary_coordinate axis. For each step,
    the energy yield is calculated by integrating the histogram. Then the yields are fitted and the sample will be moved
    to the position with minimum yield """
    type: Literal[RecipeType.minimize_yield]
    sample_id: str
    start_position: Optional[PositionCoordinates]
    file_stem: str
    total_charge: int
    vary_coordinate: VaryCoordinate
    integration_window: Window
    optimize_detector_index: int


class RbsRqmRandom(BaseModel):
    """ The model for a random measurement - the vary_coordinate will be changed"""
    type: Literal[RecipeType.random]
    sample_id: str
    file_stem: str
    start_position: Optional[PositionCoordinates]
    charge_total: int
    vary_coordinate: VaryCoordinate


class RbsRqmFixed(BaseModel):
    """ The model for a fixed measurement - all coordinates are kept the same"""
    type: Literal[RecipeType.fixed]
    sample_id: str
    file_stem: str
    charge_total: int


class RbsRqmStatus(BaseModel):
    run_status: StatusModel
    active_recipe: str
    accumulated_charge: float
    accumulated_charge_target: float


class RbsRqmSettings(BaseModel):
    rqm_number: str
    sub_folder: Optional[str]
    detectors: List[CaenDetectorModel]

    def get_folder(self):
        if self.sub_folder:
            return self.rqm_number + "/" + self.sub_folder + "/"
        else:
            return self.rqm_number + "/"


empty_settings = RbsRqmSettings(rqm_number="None", detectors=[])


class RbsRqm(BaseModel):
    recipes: List[Union[RbsRqmChanneling, RbsRqmRandom]]
    settings: RbsRqmSettings

    @classmethod
    def validate_recipes(cls, rbs_rqm):
        '''
        As of yet (2021 06), pydantic doesnt provide nice errors when using a Union. A PR is ongoing
        (https://github.com/samuelcolvin/pydantic/pull/2336) to make this better in the union definition itself.
        Consider switching to this approach when it gets released. As a temporary measure, validation of recipes now
        happens separately before creating the RbsRqm instance
        '''

        if "recipes" not in rbs_rqm:
            raise AttributeError("type object 'RbsRqm', has no attribute 'recipes'")

        for recipe in rbs_rqm["recipes"]:
            if "type" not in recipe:
                raise AttributeError("type object 'Recipes', has no attribute 'type'")
            if recipe["type"] == "random":
                RbsRqmRandom.parse_obj(recipe)
            if recipe["type"] == "channeling":
                RbsRqmChanneling.parse_obj(recipe)

    class Config:
        class Config:
            use_enum_values = True

        schema_extra = {
            'example':
                {
                    "rqm_number": "rqm_test",
                    "detectors": [
                        {"board": 1, "channel": 0, "color": "blue", "identifier": "d0",
                         "bins_min": 0, "bins_max": 1024, "bins_width": 1024},
                        {"board": 1, "channel": 1, "color": "red", "identifier": "d1",
                         "bins_min": 0, "bins_max": 1024, "bins_width": 1024}
                    ],
                    "recipes": [
                        {
                            "type": "random", "sample_id": "RBS_071A", "file_stem": "RBS_071A_out",
                            "start_position": {"x": 0},
                            "charge_total": 60000,
                            "vary_coordinate": {"name": "phi", "start": 0, "end": 30, "increment": 2},
                            "integration_window": {"start": 0, "end": 24},
                            "optimize_detector_index": 0,
                            "detector_indices": [0, 1]
                        },
                    ],
                    "parking_position": {"x": 0, "y": 0, "phi": 0, "zeta": 0, "detector": 0, "theta": 0}
                }
        }


empty_rbs_rqm = RbsRqm(recipes=[], settings=empty_settings)


class ExperimentStateModel(BaseModel):
    status: StatusModel
    experiment: RbsRqm

    class Config:
        use_enum_values = True
