from pydantic.generics import BaseModel
from pydantic import Field, validator
from typing import List, Optional
from enum import Enum

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

class Recipe(BaseModel):
    mtype: str
    ftitle: str
    x: int
    y: int
    file: str
    execution_state: Optional[str]  # pylint: disable=E1136
    phi_progress: Optional[str]  # pylint: disable=E1136
    measuring_time_sec: Optional[str]  # pylint: disable=E1136


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


class RbsModel(BaseModel):
    exp_type: str
    phi_start: int
    phi_step: int  # rename to phi_increment
    phi_end: int
    limit: int
    rqm_number: str = Field(description="This is the subfolder where the results will be stored")
    recipes: List[Recipe]
    parking_position: PositionModel
    starting_position: PositionModel
    detectors: List[CaenDetectorModel]

    class Config:
        schema_extra = {
            'example': {
                "exp_type": "rbs",
                "phi_start": 0,
                "phi_step": 1,
                "phi_end": 5,
                "limit": 100,
                "rqm_number": "some_rqm_number",
                "starting_position": {"x": 20, "y": 20, "theta": 19, "zeta": 19, "phi": 18, "det": 18},
                "detectors":
                    [
                        {"board": 1, "channel": 0, "bins_min": 0, "bins_max": 7000, "bins_width": 1024},
                        {"board": 1, "channel": 1, "bins_min": 0, "bins_max": 7000, "bins_width": 1024}
                    ],
                "recipes":
                    [
                        {"mtype": "rand", "ftitle": "ref(125,15)", "x": 1, "y": 1, "file": "RBS21_100_R1A"},
                        {"mtype": "rand", "ftitle": "d20_200cy", "x": 2, "y": 2, "file": "RBS21_100_01A"}
                    ],

                "parking_position": {"x": 20, "y": 20, "theta": 19, "zeta": 19, "phi": 18, "det": 18}
            }
        }


class StatusModel(str, Enum):
    Idle = "Idle"
    Running = "Running"
    Parking = "Parking"


class ExperimentStateModel(BaseModel):
    status: StatusModel
    experiment: RbsModel

    class Config:
        use_enum_values = True


empty_rqm = RbsModel.parse_raw('''{
"exp_type":"rbs",
"phi_start":0,
"phi_step":0,
"phi_end":0,
"limit":0,
"rqm_number":"string",
"starting_position":  {"x":0 , "y":0, "theta":0, "zeta":0, "phi":0, "det":0},
"storage":{"local":"string","remote": "string"},
"detectors": [{"board": 0, "channel":0, "bins_min":0, "bins_max":0, "bins_width":0}],
"recipes": [{"mtype":"string", "ftitle":"string" , "x":0 , "y":0  , "file":"string" }],
"parking_position":  {"x":0 , "y":0, "theta":0, "zeta":0, "phi":0, "det":0}}''')