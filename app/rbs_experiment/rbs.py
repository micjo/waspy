from typing import List
import logging
import numpy as np
import requests
import time

from app.rbs_experiment.entities import RbsHardware, CoordinateEnum, VaryCoordinate, Window
import app.hardware_controllers.hw_action as hw_action
from app.rbs_experiment.entities import CaenDetectorModel, RbsData, PositionCoordinates


def _generate_request_id() -> str:
    return datetime.datetime.now().strftime("%Y.%m.%d__%H:%M__%S.%f")


class Rbs:
    hw: RbsHardware
    detectors: List[CaenDetectorModel]
    _acquisition_run_time: float
    _acquisition_accumulated_charge: float

    def __init__(self, rbs_hw: RbsHardware):
        self.hw = rbs_hw
        self.detectors = []
        self._start_time = time.time()

    def move(self, position: PositionCoordinates):
        logging.info("Moving rbs system to '" + str(position) + "'")

        if position is None:
            return
        if position.x is not None:
            hw_action.move_aml_first(_generate_request_id(), self.hw.aml_x_y.url, position.x)
        if position.y is not None:
            hw_action.move_aml_second(_generate_request_id(), self.hw.aml_x_y.url, position.y)
        if position.phi is not None:
            hw_action.move_aml_first(_generate_request_id(), self.hw.aml_phi_zeta.url, position.phi)
        if position.zeta is not None:
            hw_action.move_aml_second(_generate_request_id(), self.hw.aml_phi_zeta.url, position.zeta)
        if position.detector is not None:
            hw_action.move_aml_first(_generate_request_id(), self.hw.aml_det_theta.url, position.detector)
        if position.theta is not None:
            hw_action.move_aml_second(_generate_request_id(), self.hw.aml_det_theta.url, position.theta)

    # def _make_histogram_meta_data(self, file_stem, sample_id, detector_id, measuring_time_msec,
    #                               total_charge) -> rbs.HistogramMetaData:
    #     aml_x_y = requests.get(self.hw.aml_x_y.url).json()
    #     aml_phi_zeta = requests.get(self.hw.aml_det_theta.url).json()
    #     aml_det_theta = requests.get(self.hw.aml_phi_zeta.url).json()
    #
    #     return HistogramMetaData(
    #         file_stem=file_stem, sample_id=sample_id, detector_id=detector_id, measuring_time_msec=measuring_time_msec,
    #         charge=total_charge,
    #         x=aml_x_y["motor_1_position"], y=aml_x_y["motor_2_position"],
    #         phi=aml_phi_zeta["motor_1_position"], zeta=aml_phi_zeta["motor_2_position"],
    #         det=aml_det_theta["motor_1_position"], theta=aml_det_theta["motor_2_position"],
    #     )

    def get_charge(self) -> float:
        motrona = requests.get(self.hw.motrona.url).json()
        return float(motrona["charge(nC)"])

    def set_active_detectors(self, detectors):
        self.detectors = detectors

    def get_histograms(self):
        histogram_data = []
        for index, detector in enumerate(self.detectors):
            data = self.get_packed_histogram(detector)
            histogram_data.append(data)
        return histogram_data

    def get_detectors(self) -> List[CaenDetectorModel]:
        return self.detectors

    def get_status(self, get_histograms=False) -> RbsData:
        aml_x_y = requests.get(self.hw.aml_x_y.url).json()
        aml_phi_zeta = requests.get(self.hw.aml_det_theta.url).json()
        aml_det_theta = requests.get(self.hw.aml_phi_zeta.url).json()
        motrona = requests.get(self.hw.motrona.url).json()
        caen = requests.get(self.hw.caen.url).json()
        histograms = []
        if get_histograms:
            histograms = self.get_histograms()

        return RbsData.parse_obj({"aml_x_y": aml_x_y, "aml_phi_zeta": aml_phi_zeta, "aml_det_theta": aml_det_theta,
                                  "motrona": motrona, "caen": caen, "detectors": self.detectors,
                                  "histograms": histograms, "measuring_time_msec": self._acquisition_run_time,
                                  "accumulated_charge": self._acquisition_accumulated_charge})

    # #TODO plotting should move out of here. plotting should be part of recipelistrunner or another class/module
    # def flush_histograms(self, settings: rbs.RbsRqmSettings, sample_id, file_stem, measuring_time_msec, total_charge):
    #     plot.set_plot_title(file_stem)
    #     histogram_data = []
    #     for index, detector in enumerate(settings.detectors):
    #         data = self.get_packed_histogram(detector)
    #         histogram_meta = self._make_histogram_meta_data(file_stem, sample_id, detector.identifier,
    #                                                         measuring_time_msec, total_charge)
    #         store.store_histogram(settings.rqm_number, histogram_meta, data)
    #         histogram_data.append(data)
    #     plot.plot_histograms(settings, file_stem, histogram_data)
    #     return histogram_data

    def count(self, count_wait_callback):
        logging.info("acquiring till target")
        hw_action.clear_start_motrona_count(_generate_request_id(), self.hw.motrona.url)
        hw_action.motrona_counting_done(self.hw.motrona.url, count_wait_callback)
        motrona = requests.get(self.hw.motrona.url).json()
        self._acquisition_accumulated_charge += float(motrona["charge(nC)"])

    def move_and_count(self, position: PositionCoordinates, count_wait_callback):
        logging.info("moving then acquiring till target")
        self.move(position)
        self.count(count_wait_callback)

    def prepare_data_acquisition(self):
        self._start_time = time.time()
        self._acquisition_accumulated_charge = 0
        hw_action.stop_clear_and_arm_caen_acquisition(_generate_request_id(), self.hw.caen.url)

    def stop_data_acquisition(self):
        self._acquisition_run_time = time.time() - self._start_time
        hw_action.stop_caen_acquisition(_generate_request_id(), self.hw.caen.url)

    def prepare_counting(self, target):
        logging.info("pause counting and set target")
        hw_action.pause_motrona_count(_generate_request_id() + "_pause", self.hw.motrona.url)
        hw_action.set_motrona_target_charge(_generate_request_id() + "_set_target_charge", self.hw.motrona.url,
                                            target)

    def get_packed_histogram(self, detector: CaenDetectorModel) -> List[int]:
        resp_code, data = hw_action.get_caen_histogram(self.hw.caen.url, detector.board, detector.channel)
        packed = hw_action.pack(data, detector.bins_min, detector.bins_max, detector.bins_width)
        return packed

    def verify_caen_boards(self, detectors: List[CaenDetectorModel]):
        for detector in detectors:
            caen_data = requests.get(self.hw.caen.url).json()
            if "board_" + str(detector['board']) not in caen_data:
                raise Exception("The specified board in the detector list does not exist")


def single_coordinate_to_string(position: PositionCoordinates, coordinate: VaryCoordinate) -> str:
    position_value = position.dict()[coordinate.name]
    return coordinate.name[0] + str(position_value)


def get_positions_as_coordinate(vary_coordinate: VaryCoordinate) -> List[PositionCoordinates]:
    angles = get_positions_as_float(vary_coordinate)
    positions = [PositionCoordinates.parse_obj({vary_coordinate.name: angle}) for angle in angles]
    return positions


def get_positions_as_float(vary_coordinate: VaryCoordinate) -> List[float]:
    if vary_coordinate.increment == 0:
        return [vary_coordinate.start]
    coordinate_range = np.arange(vary_coordinate.start, vary_coordinate.end + vary_coordinate.increment,
                                 vary_coordinate.increment)
    numpy_array = np.around(coordinate_range, decimals=2)
    return [float(x) for x in numpy_array]


def convert_float_to_coordinate(coordinate_name: str, position: float ) -> PositionCoordinates:
    return PositionCoordinates.parse_obj({coordinate_name: position})


def get_sum(data: List[int], window: Window) -> int:
    return sum(data[window.start:window.end])
