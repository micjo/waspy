from pydantic.generics import BaseModel
from pydantic import validator
from typing import List, Optional
from app.rbs_experiment.entities import CoordinateEnum, VaryCoordinate, CaenDetectorModel
from enum import Enum
import logging

import app.rbs_experiment.rbs_daemon_control as control
from app.rbs_experiment.entities import PositionCoordinates


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


async def run_experiment(task_list: ChannelingModel):
    for recipe in task_list.recipes:
        await control.move_to_position(recipe.title, recipe.start_position)
        positions = control.make_position_range(recipe.minimize_histogram.vary_coordinate)

        charge_limit_per_step = recipe.total_accumulated_charge / len(positions)
        await control.counting_pause_and_set_target(recipe.title, charge_limit_per_step)

        for index, position in enumerate(positions):
            await control.clear_and_arm_acquisition(recipe.title)
            await control.move_then_count_till_target(recipe.title + "_" + str(index), position)

            for index, detector in enumerate(task_list.detectors):
                data = await control.get_packed_histogram(detector)
                # todo: finish integration step and then do fitting


