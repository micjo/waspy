import copy
import time

import requests
from pydantic.env_settings import BaseSettings

from hive.hardware_control import http_helper as http
from hive.hardware_control.erd_entities import PositionCoordinates, ErdHardwareRoute
import logging
from threading import Lock
from hive.hardware_control.hw_action import acquisition_started, move_mdrive_done, move_mdrive


class GlobalConfig(BaseSettings):
    FAKER = False


env_conf = GlobalConfig()
faker = env_conf.FAKER


def fake_call(func, *args, **kw):
    saved_args = locals()
    time.sleep(0.1)
    logging.info("Function '" + str(saved_args) + "' faked")
    return ""


def fakeable(func):
    def wrap_func():
        if faker:
            return lambda *args, **kw: fake_call(func, args, kw)
        else:
            return func

    return wrap_func()


class ErdSetup:
    hw: ErdHardwareRoute

    def __init__(self, erd_hw: ErdHardwareRoute):
        self.hw = erd_hw
        self._lock = Lock()
        self._abort = False

    @fakeable
    def move(self, position: PositionCoordinates):
        if self._aborted():
            return
        if position is None:
            return
        logging.info("moving erd system to '" + str(position) + "'")
        if position.theta is not None:
            move_mdrive(http.generate_request_id(), self.hw.mdrive_theta.url, position.theta)
        if position.z is not None:
            move_mdrive(http.generate_request_id(), self.hw.mdrive_z.url, position.z)

    @fakeable
    def wait_for_arrival(self):
        if self._aborted():
            return
        move_mdrive_done(self.hw.mdrive_theta.url)
        move_mdrive_done(self.hw.mdrive_z.url)
        logging.info("Motors have arrived")

    def abort(self):
        with self._lock:
            self._abort = True

    def resume(self):
        with self._lock:
            self._abort = False

    def wait_for(self, seconds):
        sleep_time = 0
        while sleep_time < seconds:
            if self._aborted():
                return
            time.sleep(1)
            sleep_time += 1

    @fakeable
    def wait_for_acquisition_done(self):
        if self._aborted():
            return
        logging.info("Wait for acquisition completed")
        self._acquisition_done(self.hw.mpa3.url)
        logging.info("Acquisition completed")

    @fakeable
    def wait_for_acquisition_started(self):
        if self._aborted():
            return
        acquisition_started(self.hw.mpa3.url)
        logging.info("Acquisition Started")

    @fakeable
    def get_histogram(self):
        logging.info("get histogram")
        if self._aborted():
            return ""
        return requests.get(self.hw.mpa3.url + "/histogram", timeout=10).text

    @fakeable
    def configure_acquisition(self, measuring_time_sec: int, spectrum_filename: str):
        if self._aborted():
            return ""
        http.post_request(self.hw.mpa3.url, {
            "request_id": http.generate_request_id(),
            "halt": True,
            "erase": True,
            "run_time_enable": True,
            "set_run_time_setpoint": measuring_time_sec,
            "set_filename": spectrum_filename
        })

    @fakeable
    def reupload_config(self):
        if self._aborted():
            return ""
        http.post_request(self.hw.mpa3.url, {"request_id": http.generate_request_id(), "reupload_mpa3_cnf": True})

    @fakeable
    def start_acquisition(self):
        if self._aborted():
            return ""
        http.post_request(self.hw.mpa3.url, {"request_id": http.generate_request_id(), "start": True})

    @fakeable
    def convert_data_to_ascii(self):
        if self._aborted():
            return ""
        logging.info("Request conversion to ascii")
        http.post_request(self.hw.mpa3.url, {"request_id": http.generate_request_id(), "convert": True})
        logging.info("Conversion to ascii done")

    def get_measurement_time(self):
        mpa3 = requests.get(self.hw.mpa3.url, timeout=10).json()
        return mpa3["acquisition_status"]["real_time"]

    def _aborted(self):
        with self._lock:
            return copy.deepcopy(self._abort)

    def _acquisition_done(self, url):
        print("wait for acquisition done")
        while True:
            time.sleep(1)
            response = http.get_json(url)
            if not response["acquisition_status"]["acquiring"]:
                logging.info("Acquisition has completed")
                break
            if self._aborted():
                logging.info("acquisition done: abort requested")
                break




