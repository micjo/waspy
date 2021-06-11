from enum import Enum
from pydantic import Field, validator
from pydantic.generics import BaseModel
from typing import List, Optional


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
            raise ValueError("end must be larger than start")
        return end


class PositionCoordinates(BaseModel):
    x: Optional[float]
    y: Optional[float]
    phi: Optional[float]
    zeta: Optional[float]
    detector: Optional[float]
    theta: Optional[float]


class CoordinateEnum(str, Enum):
    zeta = "zeta"
    theta = "theta"
    phi = "phi"


class RecipeType(str, Enum):
    pre_channeling = "pre_channeling"
    channeling = "channeling"
    random = "random"


class VaryCoordinate(BaseModel):
    name: CoordinateEnum
    start: float
    end: float
    increment: float

    class Config:
        use_enum_values = True

    @validator('increment')
    def increment_must_be_positive_and_non_zero(cls, increment):
        if not increment > 0:
            raise ValueError('increment must be positive and non-zero')
        return increment

    @validator('end')
    def start_must_be_smaller_than_end(cls, end, values):
        if 'start' not in values:
            return
        if not values['start'] < end:
            raise ValueError('end must be larger than start')
        return end


class CaenDetectorModel(BaseModel):
    board: int
    channel: int
    color: str = Field(
        description="This is a matplotlib color, please refer to the docs to see which strings are valid")
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
    Parking = "Parking"


class RbsRqmRecipe(BaseModel):
    type: RecipeType
    title: str
    start_position: Optional[PositionCoordinates]
    file_stem: str
    total_charge: int
    vary_coordinate: Optional[VaryCoordinate]
    integration_window: Optional[Window]
    detector_indices: List[int]
    optimize_detector_index: Optional[int]


class RbsRqm(BaseModel):
    rqm_number: str
    detectors: List[CaenDetectorModel]
    recipes: List[RbsRqmRecipe]
    parking_position: PositionCoordinates

    class Config:
        schema_extra = {
            'example':
                {
                    "rqm_number": "rqm_test",
                    "detectors": [
                        {"board": 1, "channel": 0, "bins_min": 0, "bins_max": 1024, "bins_width": 1024},
                        {"board": 1, "channel": 1, "bins_min": 0, "bins_max": 1024, "bins_width": 1024}
                    ],
                    "recipes": [
                        {
                            "type": "pre_channeling", "title": "RBS_071A", "file_stem": "RBS_071A_out",
                            "total_charge": 60000,
                            "start_position": {"x": 0, "y": 0, "phi": 0, "zeta": 0, "detector": 0, "theta": 0},
                            "vary_coordinate": {"name": "theta", "start": 0, "end": 2, "increment": 1},
                            "integration_window": {"start": 0, "end": 24},
                            "optimize_detector_index": 0,
                            "detector_indices": [0, 1]
                        },
                        {
                            "type": "random", "title": "RBS_071B", "file_stem": "RBS_071B_out", "total_charge": 60000,
                            "vary_coordinate": {"name": "phi", "start": 0, "end": 30, "increment": 1},
                            "detector_indices": [0, 1]
                        },
                        {
                            "type": "channeling", "title": "RBS_071B", "file_stem": "RBS_071B_out",
                            "total_charge": 60000,
                            "detector_indices": [0, 1]
                        }
                    ],
                    "parking_position": {"x": 0, "y": 0, "phi": 0, "zeta": 0, "detector": 0, "theta": 0}
                }
        }


class RbsRqmStatus(BaseModel):
    run_status: StatusModel
    recipe_list: RbsRqm


empty_rbs_rqm = RbsRqm.parse_raw('''{
"rqm_number":"rqm_test",
"detectors": [],
"recipes": [],
"parking_position": {}
}''')


class ExperimentStateModel(BaseModel):
    status: StatusModel
    experiment: RbsRqm

    class Config:
        use_enum_values = True
