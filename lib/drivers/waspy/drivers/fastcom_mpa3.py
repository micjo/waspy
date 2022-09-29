import logging
import time

from waspy.drivers.http_helper import generate_request_id, post_request, get_json, get_text


class FastcomMpa3:
    """A data acquisition system"""
    _url: str

    def __init__(self, url: str):
        self._url = url

    def wait_acquisition_done(self):
        while True:
            time.sleep(1)
            if not self.acquiring():
                logging.info("Acquisition has completed")
                break

    def wait_acquisition_started(self):
        while True:
            time.sleep(1)
            if self.acquiring():
                logging.info("Acquisition has started")
                break

    def acquiring(self) -> bool:
        response = get_json(self._url)
        return response["acquisition_status"]["acquiring"]

    def stop_and_clear(self):
        request = {"request_id": generate_request_id(), "halt": True, "erase": True}
        post_request(self._url, request)

    def configure(self, measuring_time_sec: int, output_filename: str):
        request = {"request_id": generate_request_id(),
                   "run_time_enable": True,
                   "set_run_time_setpoint": measuring_time_sec,
                   "set_filename": output_filename
                   }
        post_request(self._url, request)

    def reupload_mpa3_cnf(self):
        """This re-uploads the cnf file from disk. refer to the fastcom mpa3 docs for more information"""
        post_request(self._url, {"request_id": generate_request_id(), "reupload_mpa3_cnf": True})

    def start(self):
        post_request(self._url, {"request_id": generate_request_id(), "start": True})

    def convert_data_to_ascii(self):
        post_request(self._url, {"request_id": generate_request_id(), "convert": True})

    def get_measurement_time(self):
        return get_json(self._url)["acquisition_status"]["real_time"]

    def get_histogram(self):
        return get_text(self._url + "/histogram")

    def get_status(self):
        return get_json(self._url)
