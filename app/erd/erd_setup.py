import logging
import numpy as np
import time
from pathlib import Path, WindowsPath
from typing import List

from app.erd.entities import ErdHardware, PositionCoordinates
import app.http_routes.http_helper as http


def get_z_range(start, end, increment) -> List[PositionCoordinates]:
    if increment == 0:
        return [PositionCoordinates(z=start)]
    coordinate_range = np.arange(start, end + increment, increment)
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
            logging.info("Motor has arrived")
            break


def acquisition_done(url):
    while True:
        time.sleep(1)
        response = http.get_json(url)
        if not response["acquiring"]:
            logging.info("Acquisition has completed")
            break


def acquisition_started(url):
    while True:
        time.sleep(1)
        response = http.get_json(url)
        if response["acquiring"]:
            logging.info("Acquisition has started")
            break


def fakeable(func):
    def fake_call(call, *args, **kw):
        saved_args = locals()
        time.sleep(0.1)
        logging.info("Function '" + str(saved_args) + "' faked")

    def wrap_func():
        return lambda *args, **kw: fake_call(func, args, kw)

    return wrap_func()

class ErdSetup:
    hw: ErdHardware

    def __init__(self, erd_hw: ErdHardware):
        self.hw = erd_hw

    def move(self, position: PositionCoordinates):
        if position is None:
            return
        logging.info("moving erd system to '" + str(position) + "'")
        if position.theta is not None:
            move_mdrive(http.generate_request_id(), self.hw.mdrive_theta.url, position.theta)
        if position.z is not None:
            move_mdrive(http.generate_request_id(), self.hw.mdrive_z.url, position.z)

    def wait_for_arrival(self):
        move_mdrive_done(self.hw.mdrive_theta.url)
        move_mdrive_done(self.hw.mdrive_z.url)

    def wait_for_acquisition_done(self):
        acquisition_done(self.hw.mpa3.url)

    def wait_for_acquisition_started(self):
        acquisition_started(self.hw.mpa3.url)

    def configure_acquisition(self, measuring_time_sec: int, spectrum_filename: Path):
        http.post_request(self.hw.mpa3.url, {
            "request_id": http.generate_request_id(),
            "halt": True,
            "erase": True,
            "run_time_enable": True,
            "set_run_time_set_point": measuring_time_sec,
            "set_filename": WindowsPath(spectrum_filename)
        })

    def start_acquisition(self):
        http.post_request(self.hw.mpa3.url, {"request_id": http.generate_request_id(), "start": True})


