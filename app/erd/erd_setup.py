import copy
import logging
import numpy as np
import time
from pathlib import Path, WindowsPath
from typing import List

import requests

from app.erd.entities import ErdHardware, PositionCoordinates
import app.http_routes.http_helper as http
import logging
from threading import Lock
from app.setup.config import GlobalConfig


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
    hw: ErdHardware

    def __init__(self, erd_hw: ErdHardware):
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
    def start_acquisition(self):
        if self._aborted():
            return ""
        http.post_request(self.hw.mpa3.url, {"request_id": http.generate_request_id(), "start": True})

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

    def get_measurement_time(self):
        pass


def get_z_range(start, end, increment) -> List[PositionCoordinates]:
    if increment == 0:
        return [PositionCoordinates(z=start)]
    coordinate_range = np.arange(start, end + increment, increment)
    logging.info("start: " + str(start) + ", end: " + str(end) + ", inc: " +str(increment))
    numpy_z_steps = np.around(coordinate_range, decimals=2)
    positions = [PositionCoordinates(z=float(z_step)) for z_step in numpy_z_steps]
    return positions


def move_mdrive(request_id, url: str, position: float):
    mdrive_request = {"request_id": request_id, "set_motor_target_position": position}
    http.post_request(url, mdrive_request)


def move_mdrive_done(url):
    while True:
        time.sleep(1)
        response = http.get_json(url)
        if not response["moving_to_target"]:
            logging.info("Motor '" + url + "' has arrived ")
            break


def acquisition_done(url):
    while True:
        time.sleep(1)
        response = http.get_json(url)
        if not response["acquisition_status"]["acquiring"]:
            logging.info("Acquisition has completed")
            break


def acquisition_started(url):
    while True:
        time.sleep(1)
        response = http.get_json(url)
        if response["acquisition_status"]["acquiring"]:
            logging.info("Acquisition has started")
            break

