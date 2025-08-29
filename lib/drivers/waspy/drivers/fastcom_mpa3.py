import logging
import time

from waspy.drivers.http_helper import generate_request_id, post_request, get_json, get_text


class FastcomMpa3:
    """A data acquisition system"""
    _url: str

    def __init__(self, url: str):
        self._url = url
        self._workaround_trigger = False

    def wait_acquisition_done(self):
        while True:
            time.sleep(1)
            if not self.acquiring():
                logging.info("[WASPY.DRIVERS.FASTCOM_MPA3] Acquisition has completed")
                break

    def wait_acquisition_started(self):
        while True:
            time.sleep(1)
            if self.acquiring():
                logging.info("[WASPY.DRIVERS.FASTCOM_MPA3] Acquisition has started")
                break

    def acquiring(self, acquiring_time_check=False) -> bool:
        response = get_json(self._url)
        
        acquiring = response["acquisition_status"]["acquiring"]

        if acquiring_time_check:
            # Issue with mpa3: seems that it does not report acquiring=false properly when it should
            # if run_time is larger than real_time, the acquisition should be finished. added workaround       
            real_time = response["acquisition_status"]["real_time"]
            run_time = response["acquisition_status"]["run_time"]
            if run_time > real_time and acquiring:
                logging.error("FastCom MPA3 invalid state: Acquisition should be done (run_time > real_time)"
                            "but it reports that it is still acquiring. Requesting halt")
                logging.error("FastCom MPA3 state: " + str(response))
                self._workaround_trigger = True
                self.stop()
        
        return response["acquisition_status"]["acquiring"]
        
    def get_workaround_state(self) -> bool:
        return self._workaround_trigger

    def clear_workaround_state(self):
        self._workaround_trigger = False
        
    def stop(self):
        request = {"request_id": generate_request_id(), "halt": True}
        post_request(self._url, request)


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
