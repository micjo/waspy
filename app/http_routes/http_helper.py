import time
from datetime import datetime
from typing import Dict

import requests
import hive_exception


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


def get_json_safe(url, timeout, default_value: Dict) -> Dict:
    try:
        json_value = requests.get(url, timeout=timeout).json()
    except TimeoutError as e:
        json_value = default_value
    return json_value


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
            raise hive_exception.HardwareError(url + ": " + error_message)


def post_request(url, request):
    post_dictionary(url, request)
    wait_for_request_done(url, request)


def generate_request_id() -> str:
    return datetime.now().strftime("%Y.%m.%d__%H:%M__%S.%f")