from pydantic.generics import BaseModel
from pydantic import Field
from typing import List, Optional
from enum import Enum

class SceneModel(BaseModel):
    mtype: str
    ftitle: str
    x: int
    y: int
    file: str
    execution_state: Optional[str]  # pylint: disable=E1136
    phi_progress: Optional[int] # pylint: disable=E1136
    measuring_time_msec: Optional[str] # pylint: disable=E1136

class CaenDetectorModel(BaseModel):
    board: int
    channel: int
    channel_min: int
    channel_max: int
    channel_width: int = Field(description="The range between min and max will be rescaled to this value, The bins are combined with integer sized bin intervals. values on the maximum side are potentially discared")

class EndPositionModel(BaseModel):
    x: int
    y: int
    phi: int
    zeta: int
    det: int
    theta: int

class RbsModel(BaseModel):
    exp_type: str
    phi_start: int
    phi_step: int
    phi_end: int
    limit: int
    title: str = Field(description="This is the subfolder where the results will be stored")
    storage: str = Field(description="The base folder location where the results will be stored")
    scenario: List[SceneModel]
    end_position: EndPositionModel
    detectors: List[CaenDetectorModel]
    class Config:
        schema_extra = {
            'example': {
            "exp_type":"rbs",
            "phi_start":0,
            "phi_step":1,
            "phi_end":5,
            "limit":100,
            "title":"experiment_1",
            "storage":"/home/mic/tmp/experiment_1",
            "detectors":
            [
                {"board": 1, "channel":0, "channel_min":0, "channel_max":7000, "channel_width":1024},
                {"board": 1, "channel":1, "channel_min":0, "channel_max":7000, "channel_width":1024}
            ],
            "scenario":
                [
                    {"mtype":"rand", "ftitle":"ref(125,15)" , "x":1 , "y":1  , "file":"RBS21_100_R1A" },
                    {"mtype":"rand", "ftitle":"d20_200cy"   , "x":2  , "y":2 , "file":"RBS21_100_01A" }
                ],

            "end_position":  {"x":20 , "y":20, "theta":19, "zeta":19, "phi":18, "det":18}
        }
        }

class StateEnum(str, Enum):
    Idle = "Idle"
    Running = "Running"
    Parking = "Parking"

class ExperimentStatusModel:
    state: str
    experiment: RbsModel

