from enum import Enum
from typing import List, Optional
from pydantic import BaseModel, validator
from pathlib import Path

from app.hardware_controllers.entities import SimpleConfig


class ErdHardware(BaseModel):
    mdrive_z: SimpleConfig
    mdrive_theta: SimpleConfig
    mpa3: SimpleConfig


class Erd(BaseModel):
    measuring_time_sec: int
    spectrum_filename: Path
    theta: int
    z_min: int
    z_max: int
    z_increment: int


class PositionCoordinates(BaseModel):
    z: Optional[float]
    theta: Optional[float]


class ErdRqm(BaseModel):
    recipes: List[Erd]

    class Config:
        use_enum_value = True

        schema_extra = {
            'example':
                {
                    "recipes": [
                        {
                            "measuring_time_sec": 30, "spectrum_filename": "test_001",
                            "theta": 10, "z_min": 0, "z_max": 30, "z_step": 2
                        },
                        {
                            "measuring_time_sec": 30, "spectrum_filename": "test_002",
                            "theta": 10, "z_min": 0, "z_max": 30, "z_step": 2
                        },
                    ]
                }
        }
