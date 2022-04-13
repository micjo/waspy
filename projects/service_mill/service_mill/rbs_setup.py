import copy
import logging
import time
from threading import Lock
from typing import List

import numpy as np
import requests

import hw_action as hw_action
import http_helper as http
from http_helper import generate_request_id
from rbs_entities import CaenDetectorModel, RbsData, PositionCoordinates
from rbs_entities import RbsHardware, VaryCoordinate, Window
from config import GlobalConfig

env_conf = GlobalConfig()
faker = env_conf.FAKER

def fake_call(func, *args, **kw):
    saved_args = locals()
    time.sleep(0.1)
    logging.info("Function '" + str(saved_args) + "' faked")


def fakeable(func):
    def wrap_func():
        if faker:
            return lambda *args, **kw: fake_call(func, args, kw)
        else:
            return func
    return wrap_func()


def fake_count():
    value = 0
    for i in range(0, 10):
        time.sleep(0.1)
        str_value = str(round(value, 2))
        print("fake-counter: " + str_value + " -> 10")
        data = {"charge(nC)": str_value, "target_charge(nC)": 10}
        value += 1.05


def fake_counter(func):
    def wrap_func(*args, **kwargs):
        if faker:
            return fake_count
        else:
            return func
    return wrap_func()


class RbsSetup:
    hw: RbsHardware
    detectors: List[CaenDetectorModel]
    _acquisition_run_time: float
    _acquisition_accumulated_charge: float
    _counting: bool

    def __init__(self, rbs_hw: RbsHardware):
        self.hw = rbs_hw
        self.detectors = []
        self._start_time = time.time()
        self._acquisition_run_time = 0
        self._acquisition_accumulated_charge = 0
        self.charge_offset = 0
        self._counting = False
        self._abort = False
        self._lock = Lock()

    @fakeable
    def move(self, position: PositionCoordinates):
        if self.aborted():
            return
        if position is None:
            return
        logging.info("Moving rbs system to '" + str(position) + "'")
        if position.x is not None:
            hw_action.move_aml_first(generate_request_id(), self.hw.aml_x_y.url, position.x)
        if position.y is not None:
            hw_action.move_aml_second(generate_request_id(), self.hw.aml_x_y.url, position.y)
        if position.phi is not None:
            hw_action.move_aml_first(generate_request_id(), self.hw.aml_phi_zeta.url, position.phi)
        if position.zeta is not None:
            hw_action.move_aml_second(generate_request_id(), self.hw.aml_phi_zeta.url, position.zeta)
        if position.detector is not None:
            hw_action.move_aml_first(generate_request_id(), self.hw.aml_det_theta.url, position.detector)
        if position.theta is not None:
            hw_action.move_aml_second(generate_request_id(), self.hw.aml_det_theta.url, position.theta)

    def abort(self):
        with self._lock:
            self._abort = True

    def finish(self):
        with self._lock:
            self._abort = False
        self.charge_offset = 0

    def aborted(self):
        with self._lock:
            return copy.deepcopy(self._abort)

    def _wait_for_count_finished(self):
        with self._lock:
            self._counting = True
        while True:
            time.sleep(1)
            if http.get_json(self.hw.motrona_charge.url)["status"] == "Done":
                break
            if self.aborted():
                break
        with self._lock:
            self._counting = False

    @fake_counter
    def count(self):
        if self.aborted():
            return
        logging.info("acquiring till target")
        hw_action.clear_start_motrona_count(generate_request_id(), self.hw.motrona_charge.url)
        self._wait_for_count_finished()
        motrona = requests.get(self.hw.motrona_charge.url, timeout=10).json()
        self._acquisition_accumulated_charge += float(motrona["charge(nC)"])
        self.charge_offset += float(motrona["target_charge(nC)"])

    def move_and_count(self, position: PositionCoordinates):
        self.move(position)
        self.count()

    def get_corrected_total_accumulated_charge(self):
        increment = 0
        with self._lock:
            if self._counting:
                motrona = requests.get(self.hw.motrona_charge.url, timeout=10).json()
                charge = float(motrona["charge(nC)"])
                target_charge = float(motrona["target_charge(nC)"])
                if charge < target_charge:
                    increment = charge
                else:
                    increment = target_charge
        return self.charge_offset + increment

    def initialize(self, detectors):
        self.charge_offset = 0
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
        aml_x_y = requests.get(self.hw.aml_x_y.url, timeout=10).json()
        aml_phi_zeta = requests.get(self.hw.aml_det_theta.url, timeout=10).json()
        aml_det_theta = requests.get(self.hw.aml_phi_zeta.url, timeout=10).json()
        motrona = requests.get(self.hw.motrona_charge.url, timeout=10).json()
        caen = requests.get(self.hw.caen.url, timeout=10).json()
        histograms = []
        if get_histograms:
            histograms = self.get_histograms()

        return RbsData.parse_obj({"aml_x_y": aml_x_y, "aml_phi_zeta": aml_phi_zeta, "aml_det_theta": aml_det_theta,
                                  "motrona": motrona, "caen": caen, "detectors": self.detectors,
                                  "histograms": histograms, "measuring_time_msec": self._acquisition_run_time,
                                  "accumulated_charge": self._acquisition_accumulated_charge})

    def prepare_data_acquisition(self):
        if self.aborted():
            return
        self._start_time = time.time()
        hw_action.stop_clear_and_arm_caen_acquisition(generate_request_id(), self.hw.caen.url)
        self._acquisition_accumulated_charge = 0

    def stop_data_acquisition(self):
        if self.aborted():
            return
        self._acquisition_run_time = time.time() - self._start_time
        hw_action.stop_caen_acquisition(generate_request_id(), self.hw.caen.url)

    @fakeable
    def prepare_counting(self, target):
        if self.aborted():
            return
        logging.info("pause counting and set target")
        hw_action.pause_motrona_count(generate_request_id() + "_pause", self.hw.motrona_charge.url)
        hw_action.set_motrona_target_charge(generate_request_id() + "_set_target_charge", self.hw.motrona_charge.url,
                                            target)
        logging.info("pause counting and set target done")

    def get_packed_histogram(self, detector: CaenDetectorModel) -> List[int]:
        resp_code, data = hw_action.get_caen_histogram(self.hw.caen.url, detector.board, detector.channel)
        packed = hw_action.pack(data, detector.bins_min, detector.bins_max, detector.bins_width)
        return packed

    def verify_caen_boards(self, detectors: List[CaenDetectorModel]):
        for detector in detectors:
            caen_data = requests.get(self.hw.caen.url, timeout=10).json()
            board_id = str(detector['board'])
            valid_board_ids = [board['id'] for board in caen_data['boards']]
            board_exists = any(board_id == valid_board_id for valid_board_id in valid_board_ids)
            if not board_exists:
                raise Exception("The specified board in the detector list does not exist. Actual: '" + board_id +
                                "' Expected: '" + str(valid_board_ids) + "'")


def single_coordinate_to_string(position: PositionCoordinates, coordinate: VaryCoordinate) -> str:
    position_value = position.dict()[coordinate.name]
    return coordinate.name[0] + "_" + str(position_value)


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


def convert_float_to_coordinate(coordinate_name: str, position: float) -> PositionCoordinates:
    return PositionCoordinates.parse_obj({coordinate_name: position})


def get_sum(data: List[int], window: Window) -> int:
    return sum(data[window.start:window.end])
