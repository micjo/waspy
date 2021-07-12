from typing import List
import asyncio
import logging
import math
import numpy as np

from app.setup.config import daemons
import app.hardware_controllers.daemon_comm as comm
import app.rbs_experiment.entities as rbs
import app.rbs_experiment.storing as store
import app.rbs_experiment.plotting as plot
import app.rbs_experiment.fitting as fit


async def move_to_position(identifier: str, position: rbs.PositionCoordinates):
    logging.info("Moving rbs system to '" + str(position) + "'")

    if position is None:
        return
    if position.x is not None:
        await comm.move_aml_first(identifier + "_first", daemons.aml_x_y.url, position.x)
    if position.y is not None:
        await comm.move_aml_second(identifier + "_second", daemons.aml_x_y.url, position.y)
    if position.phi is not None:
        await comm.move_aml_first(identifier + "_first", daemons.aml_phi_zeta.url, position.phi)
    if position.zeta is not None:
        await comm.move_aml_second(identifier + "_second", daemons.aml_phi_zeta.url, position.zeta)
    if position.detector is not None:
        await comm.move_aml_first(identifier + "_first", daemons.aml_det_theta.url, position.detector)
    if position.theta is not None:
        await comm.move_aml_second(identifier + "_second", daemons.aml_det_theta.url, position.theta)


async def get_and_save_histograms(sub_folder, file_stem, sample_id, measuring_time_msec,
                                  detectors: List[rbs.CaenDetectorModel]):
    plot.set_plot_title(file_stem)
    histogram_data = []
    for index, detector in enumerate(detectors):
        data = await get_packed_histogram(detector)
        await store.store_histogram(sub_folder, file_stem, sample_id, detector.identifier, measuring_time_msec, data)
        histogram_data.append(data)
    plot.plot_histograms_and_clear(sub_folder, file_stem, detectors, histogram_data)
    return histogram_data


def single_coordinate_to_string(position: rbs.PositionCoordinates, coordinate: rbs.VaryCoordinate) -> str:
    position_value = position.dict()[coordinate.name]
    return coordinate.name[0] + str(position_value)


def positions_to_floats(coordinate: rbs.CoordinateEnum, positions: List[rbs.PositionCoordinates]) -> list[float]:
    position_values = [position.dict()[coordinate] for position in positions]
    return position_values


async def get_minimum_yield_position(sub_folder, recipe: rbs.RbsRqmMinimizeYield,
                                     positions: List[rbs.PositionCoordinates],
                                     energy_yields):
    angles = positions_to_floats(recipe.vary_coordinate.name, positions)
    store.store_yields(sub_folder, recipe.file_stem, angles, energy_yields)
    smooth_angles, smooth_yields = fit.fit_and_smooth(angles, energy_yields)
    plot.plot_energy_yields(sub_folder, recipe.file_stem, angles, energy_yields, smooth_angles, smooth_yields)

    index_for_minimum_yield = np.argmin(smooth_yields)
    min_angle = round(smooth_angles[index_for_minimum_yield], 2)
    min_position = rbs.PositionCoordinates.parse_obj({recipe.vary_coordinate.name: min_angle})
    return min_position


async def get_position_range(vary_coordinate: rbs.VaryCoordinate) -> List[rbs.PositionCoordinates]:
    angles = make_coordinate_range(vary_coordinate)
    positions = [rbs.PositionCoordinates.parse_obj({vary_coordinate.name: angle}) for angle in angles]
    return positions


async def move_position_and_count(identifier: str, position: rbs.PositionCoordinates):
    logging.info("moving then acquiring till target")
    await move_to_position(identifier, position)
    await comm.clear_start_motrona_count(identifier, daemons.motrona_rbs.url)
    await comm.motrona_counting_done(daemons.motrona_rbs.url)


async def prepare_data_acquisition(identifier: str):
    await comm.stop_clear_and_arm_caen_acquisition(identifier, daemons.caen_rbs.url)


async def prepare_counting(identifier: str, target):
    logging.info("pause counting and set target")
    await comm.pause_motrona_count(identifier + "_pause", daemons.motrona_rbs.url)
    await comm.set_motrona_target_charge(identifier + "_set_target_charge", daemons.motrona_rbs.url, target)


def make_coordinate_range(vary_coordinate: rbs.VaryCoordinate) -> np.ndarray:
    coordinate_range = np.arange(vary_coordinate.start, vary_coordinate.end + vary_coordinate.increment,
                                 vary_coordinate.increment)
    return np.around(coordinate_range, decimals=2)


async def get_packed_histogram(detector: rbs.CaenDetectorModel) -> List[int]:
    data = await comm.get_caen_histogram(daemons.caen_rbs.url, detector.board, detector.channel)
    packed = pack(data, detector.bins_min, detector.bins_max, detector.bins_width)
    return packed


def get_sum(data: List[int], window: rbs.Window) -> int:
    return sum(data[window.start:window.end])


def pack(data: List[int], channel_min, channel_max, channel_width) -> List[int]:
    subset = data[channel_min:channel_max]
    samples_to_group_in_bin = math.floor(len(subset) / channel_width)
    packed_data = []
    for index in range(0, samples_to_group_in_bin * channel_width, samples_to_group_in_bin):
        bin_sum = sum(subset[index:index + samples_to_group_in_bin])
        packed_data.append(bin_sum)
    return packed_data
