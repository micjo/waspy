from pydantic.generics import BaseModel
from pydantic import validator
from typing import List, Optional
from app.rbs_experiment.entities import CoordinateEnum, VaryCoordinate, CaenDetectorModel, Window
from app.rbs_experiment.py_fitter import fit_smooth_and_minimize
from enum import Enum
import logging
import time

import app.rbs_experiment.rbs_daemon_control as control
from app.rbs_experiment.entities import PositionCoordinates


class OptimizeHistogram(BaseModel):
    """ By varying the specified coordinate, the optimal coordinate will be found where
    the window, put on top of the energy histogram, is integrated and minimized """
    vary_coordinate: VaryCoordinate
    integration_window: Window


class ChannelingRecipe(BaseModel):
    title: str
    start_position: PositionCoordinates
    file_stem: str
    total_accumulated_charge: int
    minimize_histogram: OptimizeHistogram


class ChannelingModel(BaseModel):
    rqm_number: str
    detectors: List[CaenDetectorModel]
    recipes: List[ChannelingRecipe]

    class Config:
        schema_extra = {
            'example':
                {
                    "rqm_number": "some_rqm_number",
                    "detectors":
                        [
                            {"board": 1, "channel": 0, "bins_min": 0, "bins_max": 1024, "bins_width": 1024},
                        ],
                    "recipes":
                        [
                            {
                                "title": "string",
                                "start_position": {"x": 4, "y": 5, "phi": 0, "zeta": 3, "detector": 0, "theta": 3},
                                "file_stem": "string",
                                "total_accumulated_charge": 0,
                                "minimize_histogram": {
                                    "vary_coordinate": {"name": "zeta", "start": 0, "end": 2, "increment": 1},
                                    "integration_window": {"start": 0, "end": 20}
                                }
                            },
                            {
                                "title": "string",
                                "start_position": {},
                                "file_stem": "string",
                                "total_accumulated_charge": 0,
                                "minimize_histogram": {
                                    "vary_coordinate": {"name": "theta", "start": 0, "end": 2, "increment": 1},
                                    "integration_window": {"start": 0, "end": 20}
                                }
                            }
                        ],
                }
        }


async def get_integrated_energy_yields(recipe: ChannelingRecipe, detector: CaenDetectorModel):
    await control.move_to_position(recipe.title, recipe.start_position)
    angle_values = control.make_coordinate_range(recipe.minimize_histogram.vary_coordinate)
    angle_to_vary = recipe.minimize_histogram.vary_coordinate.name

    charge_limit_per_step = recipe.total_accumulated_charge / len(angle_values)
    await control.counting_pause_and_set_target(recipe.title, charge_limit_per_step)

    energy_yields = []
    for angle in angle_values:
        await control.move_to_angle_then_acquire_till_target(recipe.title + "_" + str(angle), angle_to_vary, angle)
        time.sleep(1)
        data = await control.get_packed_histogram(detector)
        energy_yields.append(control.get_sum(data, recipe.minimize_histogram.integration_window))
    return angle_values, energy_yields


async def run_experiment(task_list: ChannelingModel):
    for recipe in task_list.recipes:
        # todo: how should the detector be described in json ? right now just take the first one from the list
        angle_values, energy_yields = await get_integrated_energy_yields(recipe, task_list.detectors[0])
        min_angle = fit_smooth_and_minimize(angle_values, energy_yields, save_plot=True, plot_x_label="test",
                                            plot_file_name="test.png")

        await control.move_to_angle("move_to_opt_angle", recipe.minimize_histogram.vary_coordinate.name, min_angle)
