from datetime import timedelta
from enum import Enum
from typing import List, Optional
from pydantic import BaseModel, validator, Field
from pathlib import Path

from app.hardware_controllers.entities import SimpleConfig, MdriveConfig


class DoublePath(BaseModel):
    local: Path
    remote: Path


class ErdHardware(BaseModel):
    mdrive_z: MdriveConfig
    mdrive_theta: MdriveConfig
    mpa3: SimpleConfig


class ErdConfig(BaseModel):
    hardware: ErdHardware
    data_dir: DoublePath


class Erd(BaseModel):
    measuring_time_sec: int
    sample_id: str
    file_stem: str
    theta: float
    z_start: float
    z_end: float
    z_increment: float


class PositionCoordinates(BaseModel):
    z: Optional[float]
    theta: Optional[float]


class ErdRqm(BaseModel):
    rqm_number: str
    recipes: List[Erd]

    class Config:
        use_enum_value = True

        schema_extra = {
            'example':
                {
                    "recipes": [
                        {
                            "rqm_number": "test_1", "measuring_time_sec": 30, "file_stem": "test_001",
                            "sample_id": "something_1", "theta": 40.00, "z_start": 1.00, "z_end": 5.00,
                            "z_increment": 0.50
                        },
                        {
                            "rqm_number": "test_2", "measuring_time_sec": 30, "file_stem": "test_002",
                            "sample_id": "something_2", "theta": 70.05, "z_start": 5.00, "z_end": 50.00,
                            "z_increment": 10.00
                        },
                    ]
                }
        }


empty_erd_rqm = ErdRqm(recipes=[], rqm_number="")


class ActiveRecipe(BaseModel):
    recipe_id: str
    run_time: timedelta
    run_time_target: float


class ErdRqmStatus(BaseModel):
    run_status: str
    active_rqm_status: List[ActiveRecipe]


empty_erd_status = ErdRqmStatus(run_status="idle", active_rqm_status=[])
