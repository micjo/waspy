from datetime import timedelta
from typing import List, Optional
from pydantic import BaseModel, Field

from entities import SimpleConfig, MdriveConfig, DoublePath


class ErdHardware(BaseModel):
    mdrive_z: MdriveConfig
    mdrive_theta: MdriveConfig
    mpa3: SimpleConfig


class ErdConfig(BaseModel):
    hardware: ErdHardware
    data_dir: DoublePath


class ErdRecipe(BaseModel):
    measuring_time_sec: int
    sample_id: str
    file_stem: str
    theta: float
    z_start: float
    z_end: float
    z_increment: float
    z_repeat: int = Field(1, description="The recipe will run from z_start to z_end, for z_repeat times.")


class PositionCoordinates(BaseModel):
    z: Optional[float]
    theta: Optional[float]


class ErdJobModel(BaseModel):
    job_id: str
    recipes: List[ErdRecipe]
    type = "erd"

    class Config:
        use_enum_value = True

        schema_extra = {
            'example':
                {
                    "rqm_number":"some_rqm",
                    "recipes": [
                        {
                            "type": "standard", "rqm_number": "test_1", "measuring_time_sec": 30,
                            "file_stem": "test_001", "sample_id": "something_1", "theta": 40.00, "z_start": 1.00,
                            "z_end": 5.00, "z_increment": 0.50
                        },
                        {
                            "type": "standard", "rqm_number": "test_2", "measuring_time_sec": 30,
                            "file_stem": "test_002", "sample_id": "something_2", "theta": 70.05, "z_start": 5.00,
                            "z_end": 50.00, "z_increment": 10.00
                        },
                    ]
                }
        }


empty_erd_rqm = ErdJobModel(recipes=[], job_id="")


class ActiveRecipe(BaseModel):
    recipe_id: str
    run_time: timedelta
    run_time_target: float


class ErdRqmStatus(BaseModel):
    run_status: str
    active_rqm_status: List[ActiveRecipe]


empty_erd_status = ErdRqmStatus(run_status="idle", active_rqm_status=[])
