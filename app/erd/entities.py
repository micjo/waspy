from enum import Enum
from typing import List, Optional
from pydantic import BaseModel, validator
from pathlib import Path

from app.hardware_controllers.entities import SimpleConfig


class ErdHardware(BaseModel):
    mdrive_z: SimpleConfig
    mdrive_theta: SimpleConfig
    mpa3: SimpleConfig


class ErdConfig(BaseModel):
    hardware: ErdHardware


class Erd(BaseModel):
    measuring_time_sec: int
    spectrum_filename: str
    theta: int
    z_start: int
    z_end: int
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
                            "theta": 40, "z_start": 1, "z_end": 1, "z_increment": 10
                        },
                        {
                            "measuring_time_sec": 30, "spectrum_filename": "test_002",
                            "theta": 70, "z_start": 10, "z_end": 2, "z_increment": 20
                        },
                    ]
                }
        }
