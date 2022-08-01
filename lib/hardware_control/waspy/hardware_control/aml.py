from waspy.hardware_control.http_helper import generate_request_id, post_request, get_json


class Aml:
    """A Stepper motor driver"""
    _url: str

    def __init__(self, url: str):
        self._url = url

    def move_first(self, target_position, wait=True):
        request = {"request_id": generate_request_id(), "set_m1_target_position": target_position}
        post_request(self._url, request, wait)

    def move_second(self, target_position, wait=True):
        request = {"request_id": generate_request_id(), "set_m2_target_position": target_position}
        post_request(self._url, request, wait)

    def load(self, wait=True):
        request = {"request_id": generate_request_id(), "m1_load": True, "m2_load": True}
        post_request(self._url, request, wait)

    def get_status(self):
        return get_json(self._url)









