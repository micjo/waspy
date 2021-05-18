from pydantic.generics import BaseModel
from pydantic import Field
from typing import List, Optional

class SceneModel(BaseModel):
    mtype: str
    ftitle: str
    x: int
    y: int
    file: str
    execution_state: Optional[str]  # pylint: disable=E1136
    phi_progress: Optional[int]

class EndPositionSchema(BaseModel):
    x: int
    y: int
    phi: int
    zeta: int
    det: int
    theta: int

class RbsSchema(BaseModel):
    exp_type: str
    phi_start: int
    phi_step: int
    phi_end: int
    limit: int
    title: str = Field(description="This is the subfolder where the results will be stored")
    storage: str = Field(description="The base folder location where the results will be stored")
    scenario: List[SceneModel]
    end_position: EndPositionSchema
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
            "scenario":
                [
                    {"mtype":"rand", "ftitle":"ref(125,15)" , "x":1 , "y":1  , "file":"RBS21_100_R1A" },
                    {"mtype":"rand", "ftitle":"d20_200cy"   , "x":2  , "y":2 , "file":"RBS21_100_01A" }
                ],

            "end_position":  {"x":20 , "y":20, "theta":19, "zeta":19, "phi":18, "det":18}
        }
        }







