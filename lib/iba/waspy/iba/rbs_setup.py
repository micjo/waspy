import copy
import logging
import time
from threading import Lock
from typing import List, Dict

import requests

from waspy.drivers.aml_smd2 import AmlSmd2
from waspy.drivers.caen import Caen
from waspy.drivers.motrona_dx350 import MotronaDx350
from waspy.iba.iba_error import IbaError
from waspy.iba.rbs_entities import Detector, RbsData, PositionCoordinates, RbsDriverUrls


def fake_call(func, *args, **kw):
    saved_args = locals()
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
    return
    for i in range(0, 3):
        time.sleep(0.1)
        str_value = str(round(value, 2))
        print("fake-counter: " + str_value + " -> 10")
        data = {"charge(nC)": str_value, "target_charge(nC)": 10}
        value += 3.05


class RbsSetup:
    detectors: List[Detector]
    _acquisition_run_time: float
    _acquisition_accumulated_charge: float
    _counting: bool
    fake: bool

    def __init__(self, rbs_hw: RbsDriverUrls):
        self.hw = rbs_hw

        self.motor_x_y = AmlSmd2(self.hw.aml_x_y.url)
        self.motor_phi_zeta = AmlSmd2(self.hw.aml_phi_zeta.url)
        self.motor_det_theta = AmlSmd2(self.hw.aml_det_theta.url)
        self.charge_counter = MotronaDx350(self.hw.motrona_charge.url)
        self.data_acquisition = Caen(self.hw.caen.url)

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
        self.motor_x_y.move_both([position.x, position.y])
        self.motor_phi_zeta.move_both([position.phi, position.zeta])
        self.motor_det_theta.move_both([position.detector, position.theta])

    def load(self):
        self.motor_x_y.load()
        self.motor_phi_zeta.load()
        self.motor_det_theta.load()

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

        while self.charge_counter.is_counting() and not self.aborted():
            time.sleep(1)

        with self._lock:
            self._counting = False

    def count(self):
        if self._fake:
            self._fake_count = 0
            return fake_counter()
        if self.aborted():
            return

        logging.info("acquiring till target")
        self.charge_counter.start_count_from_zero()
        self._wait_for_count_finished()
        self._acquisition_accumulated_charge += self.charge_counter.get_charge()
        self.charge_offset += self.charge_counter.get_target_charge()

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
                charge = self.charge_counter.get_charge()
                target_charge = self.charge_counter.get_target_charge()
                if charge < target_charge:
                    increment = charge
                else:
                    increment = target_charge
        return self.charge_offset + increment

    def clear_charge_offset(self):
        self.charge_offset = 0

    def initialize(self):
        self.charge_offset = 0

    def configure_detectors(self, detectors: List[Detector]):
        self.detectors = detectors

    def get_histograms(self) -> Dict[str, List[int]]:
        histograms = {}
        for detector in self.detectors:
            histograms[detector.identifier] = self.get_packed_histogram(detector)
        return histograms

    def get_detectors(self) -> List[Detector]:
        return self.detectors

    def get_detector(self, identifier: str) -> Detector:
        try:
            return next(detector for detector in self.detectors if detector.identifier == identifier)
        except StopIteration:
            detector_names = str([detector.identifier for detector in self.detectors])
            raise IbaError("Detector: '" + str(identifier) + "' Does not exist. Available detectors:" + detector_names)

    def get_status(self, get_histograms=False) -> RbsData:
        status_x_y = self.motor_x_y.get_status()
        status_phi_zeta = self.motor_phi_zeta.get_status()
        status_det_theta = self.motor_det_theta.get_status()

        status_charge_counter = self.charge_counter.get_status()
        status_data_acquisition = self.data_acquisition.get_status()

        histograms = []
        if get_histograms:
            histograms = self.get_histograms()
        return RbsData.parse_obj(
            {"aml_x_y": status_x_y, "aml_phi_zeta": status_phi_zeta, "aml_det_theta": status_det_theta,
             "motrona": status_charge_counter, "caen": status_data_acquisition, "detectors": self.detectors,
             "histograms": histograms, "measuring_time_msec": self._acquisition_run_time,
             "accumulated_charge": self._acquisition_accumulated_charge})

    def start_data_acquisition(self):
        if self._fake:
            return fake_call(self.start_data_acquisition)
        if self.aborted():
            return
        self._start_time = time.time()
        self.data_acquisition.restart()
        self._acquisition_accumulated_charge = 0

    def stop_data_acquisition(self):
        if self._fake:
            return fake_call(self.stop_data_acquisition)
        if self.aborted():
            return
        self._acquisition_run_time = time.time() - self._start_time
        self.data_acquisition.stop()

    def prepare_counting_with_target(self, target):
        if self._fake:
            return fake_call(self.prepare_counting_with_target, target)
        if self.aborted():
            return
        self.charge_counter.pause()
        self.charge_counter.set_target_charge(target)

    def get_packed_histogram(self, detector: Detector) -> List[int]:
        return self.data_acquisition.get_histogram(detector)

    def set_registry(self, board_id, registry_file):
        self.data_acquisition.set_registry(board_id, registry_file)

    def get_registry_value(self, board_id: str, hex_register_address: str):
        return self.data_acquisition.read_register(board_id, hex_register_address)

    def verify_detectors(self, detectors: List[Detector]):
        if not self.data_acquisition.do_detectors_exist(detectors):
            raise IbaError(f'The specified detectors({detectors}) do not (all) exist.')
