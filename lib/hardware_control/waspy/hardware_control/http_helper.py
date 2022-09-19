import time
from datetime import datetime
from typing import Dict

import requests
from requests import RequestException


class HardwareError(Exception):
    """ An exception for any hardware related requests"""
    pass


def get_text_with_response_code(url):
    response = requests.get(url, timeout=10)
    return response.status_code, response.text


def get_json_with_response_code(url):
    response = requests.get(url, timeout=10)
    return response.status_code, response.json()


def get_text(url):
    response = requests.get(url, timeout=10)
    return response.text


def get_json(url):
    return requests.get(url, timeout=10).json()


def get_json_safe(url, default_value: Dict, timeout=10) -> Dict:
    try:
        json_value = requests.get(url, timeout=timeout).json()
    except RequestException as e:
        json_value = default_value
    return json_value


def post_safe(url, json=None):
    json = json if json else {}
    try:
        response = requests.post(url, timeout=10, json=json)
        return response.status_code, response.text
    except RequestException as e:
        return 400, ""


def post_dictionary(url, data):
    response = requests.post(url, json=data, timeout=10)
    return response.status_code, response.text


def wait_for_request_done(url, request):
    while True:
        time.sleep(0.2)
        response = get_json(url)
        error_message = response["error"]
        if error_message == "Success" or error_message == "No error":
            if response['request_finished'] and response["request_id"] == str(request["request_id"]):
                break
        else:
            raise HardwareError(url + ": " + error_message)


def post_request(url, request, wait=True):
    post_dictionary(url, request)
    if wait:
        wait_for_request_done(url, request)


def generate_request_id() -> str:
    return datetime.now().strftime("%Y.%m.%d__%H:%M__%S.%f")
