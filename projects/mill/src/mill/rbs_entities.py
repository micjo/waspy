from datetime import timedelta
from pathlib import Path
from enum import Enum
from typing import List, Optional, Union, Literal, Annotated

from pydantic import Field, validator
from pydantic.generics import BaseModel

from mill.entities import SimpleConfig, AmlConfig, CaenConfig
from waspy.iba.rbs_entities import PositionCoordinates, RbsChanneling, RbsRandom


class RbsDriverGroup(BaseModel):
    aml_x_y: AmlConfig
    aml_phi_zeta: AmlConfig
    aml_det_theta: AmlConfig
    caen: CaenConfig
    motrona_charge: SimpleConfig


class RbsConfig(BaseModel):
    local_dir: Path
    remote_dir: Path
    drivers: RbsDriverGroup


class StatusModel(str, Enum):
    Idle = "Idle"
    Running = "Running"


class RbsJobModel(BaseModel):
    recipes: List[Annotated[Union[RbsChanneling, RbsRandom], Field(discriminator='type')]]
    name: str
    type = "rbs"

    class Config:
        use_enum_values = True

        schema_extra = {
            'example':
                {
                    "name": "RBS21_071", "type": "rbs",
                    "recipes": [
                        {"type": "rbs_random", "sample": "AE007607_D02_A", "name": "RBS21_071_01B_A",
                         "start_position": {"x": 10, "y": 22, "phi": 0}, "charge_total": 45000,
                         "vary_coordinate": {"name": "phi", "start": 0, "end": 30, "increment": 2}
                         },
                        {"type": "rbs_random", "sample": "AE007607_D02_B", "name": "RBS21_071_08B_A",
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
