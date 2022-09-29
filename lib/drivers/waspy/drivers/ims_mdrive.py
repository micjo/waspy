import time

from waspy.drivers.http_helper import generate_request_id, post_request, get_json


class ImsMDrive:
    """A Stepper motor driver"""
    _url: str

    def __init__(self, url: str):
        self._url = url

    def move(self, target_position, wait=True):
        if target_position is None:
            return
        request = {"request_id": generate_request_id(), "set_motor_target_position": target_position}
        post_request(self._url, request)
        if wait:
            self.move_done()

    def load(self, wait=True):
        request = {"request_id": generate_request_id(), "load": True}
        post_request(self._url, request)
        if wait:
            self.move_done()

    def wait_for_move_done(self):
        while True:
            time.sleep(1)
            response = get_json(self._url)
            if not response["moving_to_target"]:
                break

    def get_status(self):
        return get_json(self._url)
