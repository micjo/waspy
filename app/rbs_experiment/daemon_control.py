from typing import List
import asyncio
import logging
import math
import numpy as np

from app.setup.config import daemons
import app.hardware_controllers.daemon_comm as comm
import app.rbs_experiment.entities as rbs


async def move_to_position(identifier: str, position: rbs.PositionCoordinates):
    logging.info("Moving rbs system to '" + str(position) + "'")
    print("Moving rbs system to '" + str(position) + "'")

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


async def move_to_angle(identifier: str, coordinate: rbs.CoordinateEnum, value):
    if coordinate == rbs.CoordinateEnum.phi:
        await move_to_position(identifier, rbs.PositionCoordinates(phi=value))
    if coordinate == rbs.CoordinateEnum.zeta:
        await move_to_position(identifier, rbs.PositionCoordinates(zeta=value))
    if coordinate == rbs.CoordinateEnum.theta:
        await move_to_position(identifier, rbs.PositionCoordinates(theta=value))


async def move_to_angle_then_acquire_till_target(identifier: str, coordinate: rbs.CoordinateEnum, value):
    logging.info("moving then acquiring till target")
    print("moving then acquiring till target")
    await move_to_angle(identifier, coordinate, value)
    await comm.clear_start_motrona_count(identifier, daemons.motrona_rbs.url)
    await comm.motrona_counting_done(daemons.motrona_rbs.url)


async def stop_clear_and_arm_caen_acquisition(identifier: str):
    await comm.stop_clear_and_arm_caen_acquisition(identifier, daemons.caen_rbs.url)


async def counting_pause_and_set_target(identifier: str, target):
    logging.info("pause counting and set target")
    print("pause counting and set target")
    await comm.pause_motrona_count(identifier + "_pause", daemons.motrona_rbs.url)
    await comm.set_motrona_target_charge(identifier + "_set_target_charge", daemons.motrona_rbs.url, target)


def make_coordinate_range(vary_coordinate: rbs.VaryCoordinate) -> List[float]:
    coordinate_range = np.arange(vary_coordinate.start, vary_coordinate.end + vary_coordinate.increment,
                                 vary_coordinate.increment)
    return np.around(coordinate_range, decimals=2)


async def get_packed_histogram(detector: rbs.CaenDetectorModel) -> List[int]:
    print("zzzz - waiting for some caen data")
    logging.info("zzz - waiting for some caen data")
    await asyncio.sleep(2)
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
