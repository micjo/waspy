import copy
import time
from pydantic.env_settings import BaseSettings

import logging
from threading import Lock

from waspy.drivers.fastcom_mpa3 import FastcomMpa3
from waspy.drivers.ims_mdrive import ImsMDrive
from waspy.iba.erd_entities import ErdDriverUrls, PositionCoordinates, ErdData


class GlobalConfig(BaseSettings):
    FAKER = False


env_conf = GlobalConfig()
faker = env_conf.FAKER


def fake_call(func, *args, **kw):
    saved_args = locals()
    time.sleep(0.1)
    logging.info("Function '" + str(saved_args) + "' faked")
    return ""


class ErdSetup:
    _fake: bool
    _fake_count: int

    def __init__(self, erd_driver_urls: ErdDriverUrls):
        self.mdrive_z = ImsMDrive(erd_driver_urls.mdrive_z.url)
        self.mdrive_theta = ImsMDrive(erd_driver_urls.mdrive_theta.url)
        self.mpa3 = FastcomMpa3(erd_driver_urls.mpa3.url)
        self._lock = Lock()
        self._abort = False
        self._fake = False
        self._fake_count = 0

    def fake(self):
        self._fake = True

    def move(self, position: PositionCoordinates):
        if self._fake:
            return fake_call(self.move, position)
        if self._aborted():
            return
        if position is None:
            return
        logging.info("moving erd system to '" + str(position) + "'")
        self.mdrive_z.move(position.z)
        self.mdrive_theta.move(position.theta)

    def load(self):
        self.mdrive_z.load()
        self.mdrive_theta.load()

    def get_status(self, get_histogram=False) -> ErdData:
        status_mdrive_z = self.mdrive_z.get_status()
        status_mdrive_theta = self.mdrive_theta.get_status()
        status_mpa3 = self.mpa3.get_status()

        histogram = ""
        if get_histogram:
            histogram = self.get_histogram()
        return ErdData.parse_obj(
            {"mdrive_z": status_mdrive_z, "mdrive_theta": status_mdrive_theta, "mpa3": status_mpa3,
             "histogram": histogram, "measuring_time_sec": self.get_measurement_time()})

    def wait_for_arrival(self):
        if self._fake:
            return fake_call(self.wait_for_arrival)
        if self._aborted():
            return

        self.mdrive_theta.wait_for_move_done()
        self.mdrive_z.wait_for_move_done()
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

    def wait_for_acquisition_done(self):
        if self._fake:
            return fake_call(self.wait_for_acquisition_done)
        if self._aborted():
            return
        logging.info("Wait for acquisition completed")
        self._acquisition_done(self.hw.mpa3.url)
        logging.info("Acquisition completed")

    def wait_for_acquisition_started(self):
        if self._fake:
            return fake_call(self.wait_for_acquisition_started)
        if self._aborted():
            return
        acquisition_started(self.hw.mpa3.url)
        logging.info("Acquisition Started")

    def get_histogram(self):
        if self._fake:
            return fake_call(self.get_histogram)
        logging.info("get histogram")
        if self._aborted():
            return ""
        return self.mpa3.get_histogram()

    def configure_acquisition(self, measuring_time_sec: int, spectrum_filename: str):
        if self._fake:
            return fake_call(self.configure_acquisition)
        if self._aborted():
            return ""
        self.mpa3.stop_and_clear()
        self.mpa3.configure(measuring_time_sec, spectrum_filename)

    def reupload_config(self):
        if self._fake:
            return fake_call(self.reupload_config)
        if self._aborted():
            return ""
        self.mpa3.reupload_mpa3_cnf()

    def initialize(self):
        self.reupload_config()

    def start_acquisition(self):
        if self._fake:
            self._fake_count = 0
            return fake_call(self.start_acquisition)
        if self._aborted():
            return ""
        self.mpa3.start()

    def convert_data_to_ascii(self):
        if self._fake:
            return fake_call(self.convert_data_to_ascii)
        if self._aborted():
            return ""
        logging.info("Request conversion to ascii")
        self.mpa3.convert_data_to_ascii()
        logging.info("Conversion to ascii done")

    def get_measurement_time(self):
        return self.mpa3.get_measurement_time()

    def _aborted(self):
        with self._lock:
            return copy.deepcopy(self._abort)

    def _acquisition_done(self, url):
        print("wait for acquisition done")
        while True:
            time.sleep(1)
            if not self.mpa3.acquiring():
                logging.info("Acquisition has completed")
                break
            if self._aborted():
                logging.info("acquisition done: abort requested")
                break
