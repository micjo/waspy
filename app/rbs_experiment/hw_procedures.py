from typing import List
import logging
import numpy as np

from app.setup.config import cfg
import app.hardware_controllers.hw_control as hw_control
import app.rbs_experiment.entities as rbs
import app.rbs_experiment.yield_store as store
import app.rbs_experiment.yield_plot as plot
import app.rbs_experiment.yield_angle_fit as fit


async def move_to_position(identifier: str, position: rbs.PositionCoordinates):
    logging.info("Moving rbs system to '" + str(position) + "'")

    if position is None:
        return
    if position.x is not None:
        await hw_control.move_aml_first(identifier + "_first", cfg.daemons.aml_x_y.url, position.x)
    if position.y is not None:
        await hw_control.move_aml_second(identifier + "_second", cfg.daemons.aml_x_y.url, position.y)
    if position.phi is not None:
        await hw_control.move_aml_first(identifier + "_first", cfg.daemons.aml_phi_zeta.url, position.phi)
    if position.zeta is not None:
        await hw_control.move_aml_second(identifier + "_second", cfg.daemons.aml_phi_zeta.url, position.zeta)
    if position.detector is not None:
        await hw_control.move_aml_first(identifier + "_first", cfg.daemons.aml_det_theta.url, position.detector)
    if position.theta is not None:
        await hw_control.move_aml_second(identifier + "_second", cfg.daemons.aml_det_theta.url, position.theta)


async def _make_histogram_meta_data(file_stem, sample_id, detector_id, measuring_time_msec) -> rbs.HistogramMetaData:
    aml_x_y = await hw_control.get_json_status(cfg.daemons.aml_x_y)
    aml_phi_zeta = await hw_control.get_json_status(cfg.daemons.aml_det_theta)
    aml_det_theta = await hw_control.get_json_status(cfg.daemons.aml_phi_zeta)
    motrona = await hw_control.get_json_status(cfg.daemons.motrona_rbs)

    return rbs.HistogramMetaData(
        file_stem=file_stem, sample_id=sample_id, detector_id=detector_id, measuring_time_msec=measuring_time_msec,
        charge=motrona["charge(nc)"],
        x=aml_x_y["motor_1_position"], y=aml_x_y["motor_2_position"],
        phi=aml_phi_zeta["motor_1_position"], zeta=aml_phi_zeta["motor_2_position"],
        det=aml_det_theta["motor_1_position"], theta=aml_det_theta["motor_2_position"],
    )


async def get_and_save_histograms(sub_folder, file_stem, sample_id, measuring_time_msec,
                                  detectors: List[rbs.CaenDetectorModel]):
    plot.set_plot_title(file_stem)
    histogram_data = []
    for index, detector in enumerate(detectors):
        data = await get_packed_histogram(detector)
        histogram_meta = await _make_histogram_meta_data(file_stem, sample_id, detector.identifier, measuring_time_msec)
        await store.store_histogram(sub_folder, histogram_meta, data)
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

    min_angle = fit.get_angle_for_minimum_yield(smooth_angles, smooth_yields)
    min_position = rbs.PositionCoordinates.parse_obj({recipe.vary_coordinate.name: min_angle})
    return min_position


async def get_position_range(vary_coordinate: rbs.VaryCoordinate) -> List[rbs.PositionCoordinates]:
    angles = make_coordinate_range(vary_coordinate)
    positions = [rbs.PositionCoordinates.parse_obj({vary_coordinate.name: angle}) for angle in angles]
    return positions


async def count(identifier: str, count_wait_callback):
    logging.info("moving then acquiring till target")
    await hw_control.clear_start_motrona_count(identifier, cfg.daemons.motrona_rbs.url)
    await hw_control.motrona_counting_done(cfg.daemons.motrona_rbs.url, count_wait_callback)


async def move_position_and_count(identifier: str, position: rbs.PositionCoordinates, count_wait_callback):
    logging.info("moving then acquiring till target")
    await move_to_position(identifier, position)
    await hw_control.clear_start_motrona_count(identifier, cfg.daemons.motrona_rbs.url)
    await hw_control.motrona_counting_done(cfg.daemons.motrona_rbs.url, count_wait_callback)


async def prepare_data_acquisition(identifier: str):
    await hw_control.stop_clear_and_arm_caen_acquisition(identifier, cfg.daemons.caen_rbs.url)


async def prepare_counting(identifier: str, target):
    logging.info("pause counting and set target")
    await hw_control.pause_motrona_count(identifier + "_pause", cfg.daemons.motrona_rbs.url)
    await hw_control.set_motrona_target_charge(identifier + "_set_target_charge", cfg.daemons.motrona_rbs.url, target)


def make_coordinate_range(vary_coordinate: rbs.VaryCoordinate) -> np.ndarray:
    coordinate_range = np.arange(vary_coordinate.start, vary_coordinate.end + vary_coordinate.increment,
                                 vary_coordinate.increment)
    return np.around(coordinate_range, decimals=2)


async def get_packed_histogram(detector: rbs.CaenDetectorModel) -> List[int]:
    resp_code, data = await hw_control.get_caen_histogram(cfg.daemons.caen_rbs.url, detector.board, detector.channel)
    packed = hw_control.pack(data, detector.bins_min, detector.bins_max, detector.bins_width)
    return packed


def get_sum(data: List[int], window: rbs.Window) -> int:
    return sum(data[window.start:window.end])


async def verify_caen_boards(detectors: List[rbs.CaenDetectorModel]):
    for detector in detectors:
        caen_data = await hw_control.get_json_status(cfg.daemons.caen_rbs.url)
        if "board_" + str(detector['board']) not in caen_data:
            raise Exception("The specified board in the detector list does not exist")


async def get_all_json_status():
    status = {}
    for any_key, any_daemon in cfg.daemons:
        status[any_key] = hw_control.get_json_status(any_daemon.url)
    return status
