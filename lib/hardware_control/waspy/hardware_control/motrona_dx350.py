from time import sleep
from waspy.hardware_control.http_helper import generate_request_id, post_request, get_json


class MotronaDx350:
    """A pulse/charge counter"""
    _url: str

    def __init__(self, url: str):
        self._url = url

    def start_count_from_zero(self):
        request = {"request_id": generate_request_id(), "clear-start_counting": True}
        post_request(self._url, request)

    def start_count(self):
        request = {"request_id": generate_request_id(), "start_counting": True}
        post_request(self._url, request)

    def pause(self):
        request = {"request_id": generate_request_id(), "pause_counting": True}
        post_request(self._url, request)

    def counting_done(self):
        while True:
            sleep(1)
            response = get_json(self._url)
            if response["status"] == "Done":
                break

    def set_target_charge(self, target_charge):
        request = {"request_id": generate_request_id(), "target_charge": target_charge}
        post_request(self._url, request)

    def get_status(self):
        return get_json(self._url)
