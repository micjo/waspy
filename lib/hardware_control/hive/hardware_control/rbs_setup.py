import copy
import logging
import time
from threading import Lock
from typing import List

import requests
from pydantic.env_settings import BaseSettings

from hive.hardware_control.http_helper import generate_request_id, get_json
from hive.hardware_control.rbs_entities import CaenDetectorModel, RbsData, PositionCoordinates, \
    RbsHardwareRoute, HistogramData
from hive.hardware_control.hw_action import move_aml_first, move_aml_second, clear_start_motrona_count, \
    stop_clear_and_arm_caen_acquisition, stop_caen_acquisition, pause_motrona_count, set_motrona_target_charge, \
    get_packed_histogram, caen_set_registry, caen_read_single_register, load_aml


def fake_call(func, *args, **kw):
    saved_args = locals()
    time.sleep(0.1)
    logging.info("Function '" + str(saved_args) + "' faked")


def fakeable(func, faker):
    def wrap_func():
        if faker:
            return lambda *args, **kw: fake_call(func, args, kw)
        else:
            return func

    return wrap_func()


def fake_counter():
    value = 0
    for i in range(0, 10):
        time.sleep(0.1)
        str_value = str(round(value, 2))
        print("fake-counter: " + str_value + " -> 10")
        data = {"charge(nC)": str_value, "target_charge(nC)": 10}
        value += 1.05


class RbsSetup:
    hw: RbsHardwareRoute
    detectors: List[CaenDetectorModel]
    _acquisition_run_time: float
    _acquisition_accumulated_charge: float
    _counting: bool
    fake: bool

    def __init__(self, rbs_hw: RbsHardwareRoute):
        self.hw = rbs_hw
        self.detectors = []
        self._start_time = time.time()
        self._acquisition_run_time = 0
        self._acquisition_accumulated_charge = 0
        self.charge_offset = 0
        self._counting = False
        self._abort = False
        self._lock = Lock()
        self._fake = False
        self._fake_count = 0

    def fake(self):
        self._fake = True

    def move(self, position: PositionCoordinates):
        if self._fake:
            return fake_call(self.move, position)
        if self.aborted():
            return
        if position is None:
            return
        logging.info("Moving rbs system to '" + str(position) + "'")
        if position.x is not None:
            move_aml_first(generate_request_id(), self.hw.aml_x_y.url, position.x)
        if position.y is not None:
            move_aml_second(generate_request_id(), self.hw.aml_x_y.url, position.y)
        if position.phi is not None:
            move_aml_first(generate_request_id(), self.hw.aml_phi_zeta.url, position.phi)
        if position.zeta is not None:
            move_aml_second(generate_request_id(), self.hw.aml_phi_zeta.url, position.zeta)
        if position.detector is not None:
            move_aml_first(generate_request_id(), self.hw.aml_det_theta.url, position.detector)
        if position.theta is not None:
            move_aml_second(generate_request_id(), self.hw.aml_det_theta.url, position.theta)

    def load(self):
        load_aml(generate_request_id(), self.hw.aml_x_y.url)
        load_aml(generate_request_id(), self.hw.aml_phi_zeta.url)
        load_aml(generate_request_id(), self.hw.aml_det_theta.url)

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
            if get_json(self.hw.motrona_charge.url)["status"] == "Done":
                break
            if self.aborted():
                break
        with self._lock:
            self._counting = False

    def count(self):
        if self._fake:
            self._fake_count = 0
            return fake_counter()
        if self.aborted():
            return
        logging.info("acquiring till target")
        clear_start_motrona_count(generate_request_id(), self.hw.motrona_charge.url)
        self._wait_for_count_finished()
        motrona = get_json(self.hw.motrona_charge.url)
        self._acquisition_accumulated_charge += float(motrona["charge(nC)"])
        self.charge_offset += float(motrona["target_charge(nC)"])

    def move_and_count(self, position: PositionCoordinates):
        self.move(position)
        self.count()

    def get_corrected_total_accumulated_charge(self):
        increment = 0
        if self._fake:
            self._fake_count += 10
            return self._fake_count
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

    def initialize(self, detectors: List[CaenDetectorModel]):
        self.charge_offset = 0
        self.detectors = detectors

    def get_histograms(self) -> List[HistogramData]:
        histogram_data = []
        for detector in self.detectors:
            data = self.get_packed_histogram(detector)
            title = detector.identifier
            histogram_data.append(HistogramData(data=data, title=title))
        return histogram_data

    def get_detectors(self) -> List[CaenDetectorModel]:
        return self.detectors

    def get_status(self, get_histograms=False) -> RbsData:
        aml_x_y = get_json(self.hw.aml_x_y.url)
        aml_phi_zeta = get_json(self.hw.aml_phi_zeta.url)
        aml_det_theta = get_json(self.hw.aml_det_theta.url)
        motrona = get_json(self.hw.motrona_charge.url)
        caen = get_json(self.hw.caen.url)
        histograms = []
        if get_histograms:
            histograms = self.get_histograms()

        return RbsData.parse_obj({"aml_x_y": aml_x_y, "aml_phi_zeta": aml_phi_zeta, "aml_det_theta": aml_det_theta,
                                  "motrona": motrona, "caen": caen, "detectors": self.detectors,
                                  "histograms": histograms, "measuring_time_msec": self._acquisition_run_time,
                                  "accumulated_charge": self._acquisition_accumulated_charge})

    def start_data_acquisition(self):
        if self.aborted():
            return
        self._start_time = time.time()
        stop_clear_and_arm_caen_acquisition(generate_request_id(), self.hw.caen.url)
        self._acquisition_accumulated_charge = 0

    def stop_data_acquisition(self):
        if self.aborted():
            return
        self._acquisition_run_time = time.time() - self._start_time
        stop_caen_acquisition(generate_request_id(), self.hw.caen.url)

    def prepare_counting_with_target(self, target):
        if self._fake:
            return fake_call(self.prepare_counting_with_target, target)
        if self.aborted():
            return
        logging.info("pause counting and set target")
        pause_motrona_count(generate_request_id() + "_pause", self.hw.motrona_charge.url)
        set_motrona_target_charge(generate_request_id() + "_set_target_charge", self.hw.motrona_charge.url, target)
        logging.info("pause counting and set target done")

    def get_packed_histogram(self, detector: CaenDetectorModel) -> List[int]:
        _, packed = get_packed_histogram(self.hw.caen.url, detector)
        return packed

    def set_registry(self, board_id, registry_file):
        caen_set_registry(generate_request_id(), self.hw.caen.url, board_id, registry_file)

    def get_registry_value(self, board_id:str, hex_register_address:str):
        caen_read_single_register(generate_request_id(), self.hw.caen.url, board_id, hex_register_address)

    def verify_caen_boards(self, detectors: List[CaenDetectorModel]):
        for detector in detectors:
            caen_data = get_json(self.hw.caen.url)
            board_id = str(detector['board'])
            valid_board_ids = [board['id'] for board in caen_data['boards']]
            board_exists = any(board_id == valid_board_id for valid_board_id in valid_board_ids)
            if not board_exists:
                raise Exception("The specified board in the detector list does not exist. Actual: '" + board_id +
                                "' Expected: '" + str(valid_board_ids) + "'")


