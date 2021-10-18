from typing import List
import logging
import numpy as np
import datetime
import requests

from app.rbs_experiment.entities import RbsConfig
import app.hardware_controllers.hw_action as hw_action
import app.rbs_experiment.entities as rbs
import app.rbs_experiment.yield_store as store
import app.rbs_experiment.yield_plot as plot
import app.rbs_experiment.yield_angle_fit as fit


def _generate_request_id() -> str:
    return datetime.datetime.now().strftime("%Y.%m.%d__%H:%M__%S.%f")


class Rbs:
    config: RbsConfig

    def __init__(self, rbs_config: rbs.RbsConfig):
        self.config = rbs_config

    def move(self, position: rbs.PositionCoordinates):
        logging.info("Moving rbs system to '" + str(position) + "'")

        if position is None:
            return
        if position.x is not None:
            hw_action.move_aml_first(_generate_request_id(), self.config.aml_x_y.url, position.x)
        if position.y is not None:
            hw_action.move_aml_second(_generate_request_id(), self.config.aml_x_y.url, position.y)
        if position.phi is not None:
            hw_action.move_aml_first(_generate_request_id(), self.config.aml_phi_zeta.url, position.phi)
        if position.zeta is not None:
            hw_action.move_aml_second(_generate_request_id(), self.config.aml_phi_zeta.url, position.zeta)
        if position.detector is not None:
            hw_action.move_aml_first(_generate_request_id(), self.config.aml_det_theta.url, position.detector)
        if position.theta is not None:
            hw_action.move_aml_second(_generate_request_id(), self.config.aml_det_theta.url, position.theta)

    def _make_histogram_meta_data(self, file_stem, sample_id, detector_id, measuring_time_msec,
                                  total_charge) -> rbs.HistogramMetaData:
        aml_x_y = requests.get(self.config.aml_x_y.url).json()
        aml_phi_zeta = requests.get(self.config.aml_det_theta.url).json()
        aml_det_theta = requests.get(self.config.aml_phi_zeta.url).json()

        return rbs.HistogramMetaData(
            file_stem=file_stem, sample_id=sample_id, detector_id=detector_id, measuring_time_msec=measuring_time_msec,
            charge=total_charge,
            x=aml_x_y["motor_1_position"], y=aml_x_y["motor_2_position"],
            phi=aml_phi_zeta["motor_1_position"], zeta=aml_phi_zeta["motor_2_position"],
            det=aml_det_theta["motor_1_position"], theta=aml_det_theta["motor_2_position"],
        )

    def get_charge(self) -> float:
        motrona = requests.get(self.config.motrona.url).json()
        return float(motrona["charge(nC)"])

    def flush_histograms(self, settings: rbs.RbsRqmSettings, sample_id, file_stem, measuring_time_msec, total_charge):
        plot.set_plot_title(file_stem)
        histogram_data = []
        for index, detector in enumerate(settings.detectors):
            data = self.get_packed_histogram(detector)
            histogram_meta = self._make_histogram_meta_data(file_stem, sample_id, detector.identifier,
                                                            measuring_time_msec, total_charge)
            store.store_histogram(settings.rqm_number, histogram_meta, data)
            histogram_data.append(data)
        plot.plot_histograms_and_clear(settings, file_stem, histogram_data)
        return histogram_data

    def count(self, count_wait_callback):
        logging.info("acquiring till target")
        hw_action.clear_start_motrona_count(_generate_request_id(), self.config.motrona.url)
        hw_action.motrona_counting_done(self.config.motrona.url, count_wait_callback)

    def move_and_count(self, position: rbs.PositionCoordinates, count_wait_callback):
        logging.info("moving then acquiring till target")
        self.move(position)
        hw_action.clear_start_motrona_count(_generate_request_id(), self.config.motrona.url)
        hw_action.motrona_counting_done(self.config.motrona.url, count_wait_callback)

    def prepare_data_acquisition(self):
        hw_action.stop_clear_and_arm_caen_acquisition(_generate_request_id(), self.config.caen.url)

    def stop_data_acquisition(self):
        hw_action.stop_caen_acquisition(_generate_request_id(), self.config.caen.url)

    def prepare_counting(self, target):
        logging.info("pause counting and set target")
        hw_action.pause_motrona_count(_generate_request_id() + "_pause", self.config.motrona.url)
        hw_action.set_motrona_target_charge(_generate_request_id() + "_set_target_charge", self.config.motrona.url,
                                            target)

    def get_packed_histogram(self, detector: rbs.CaenDetectorModel) -> List[int]:
        resp_code, data = hw_action.get_caen_histogram(self.config.caen.url, detector.board, detector.channel)
        packed = hw_action.pack(data, detector.bins_min, detector.bins_max, detector.bins_width)
        return packed

    def verify_caen_boards(self, detectors: List[rbs.CaenDetectorModel]):
        for detector in detectors:
            caen_data = requests.get(self.config.caen.url).json()
            if "board_" + str(detector['board']) not in caen_data:
                raise Exception("The specified board in the detector list does not exist")


def single_coordinate_to_string(position: rbs.PositionCoordinates, coordinate: rbs.VaryCoordinate) -> str:
    position_value = position.dict()[coordinate.name]
    return coordinate.name[0] + str(position_value)


def positions_to_floats(coordinate: rbs.CoordinateEnum, positions: List[rbs.PositionCoordinates]) -> list[float]:
    position_values = [position.dict()[coordinate] for position in positions]
    return position_values


def get_minimum_yield_position(sub_folder, recipe: rbs.RbsRqmMinimizeYield,
                               positions: List[rbs.PositionCoordinates],
                               energy_yields):
    angles = positions_to_floats(recipe.vary_coordinate.name, positions)
    store.store_yields(sub_folder, recipe.file_stem, angles, energy_yields)
    smooth_angles, smooth_yields = fit.fit_and_smooth(angles, energy_yields)
    plot.plot_energy_yields(sub_folder, recipe.file_stem, angles, energy_yields, smooth_angles, smooth_yields)
    min_angle = fit.get_angle_for_minimum_yield(smooth_angles, smooth_yields)
    min_position = rbs.PositionCoordinates.parse_obj({recipe.vary_coordinate.name: min_angle})
    return min_position


def get_position_range(vary_coordinate: rbs.VaryCoordinate) -> List[rbs.PositionCoordinates]:
    angles = make_coordinate_range(vary_coordinate)
    positions = [rbs.PositionCoordinates.parse_obj({vary_coordinate.name: angle}) for angle in angles]
    return positions


def make_coordinate_range(vary_coordinate: rbs.VaryCoordinate) -> np.ndarray:
    if vary_coordinate.increment == 0:
        return np.array([vary_coordinate.start])
    coordinate_range = np.arange(vary_coordinate.start, vary_coordinate.end + vary_coordinate.increment,
                                 vary_coordinate.increment)
    return np.around(coordinate_range, decimals=2)


def get_sum(data: List[int], window: rbs.Window) -> int:
    return sum(data[window.start:window.end])
