import math
from typing import List, Any

import logging
import time
import app.http_routes.http_helper as http

logging.basicConfig(level=logging.INFO, filename="debug.log")

faker_time = 0.2
faker = False


def wait_for_request_done(url, request):
    while True:
        time.sleep(0.2)
        response = http.get_json(url)
        error_message = response["error"]
        if error_message == "Success" or error_message == "No error":
            if response['request_finished'] and response["request_id"] == str(request["request_id"]):
                break
        else:
            raise Exception(url + ": " + error_message)


def post_request(url, request):
    logging.info("post to: " + url + ", content: " + str(request))
    if faker:
        time.sleep(faker_time)
        return

    http.post_dictionary(url, request)
    wait_for_request_done(url, request)


def set_motrona_target_charge(request_id, url, target_charge):
    motrona_request = {"request_id": request_id, "target_charge": target_charge}
    post_request(url, motrona_request)


def move_aml_first(request_id, url, position):
    aml_request = {"request_id": request_id, "set_m1_target_position": position}
    post_request(url, aml_request)


def move_aml_second(request_id, url, position):
    aml_request = {"request_id": request_id, "set_m2_target_position": position}
    post_request(url, aml_request)


def move_aml_both(request_id, url, positions):
    aml_request = {"request_id": request_id, "set_m1_target_position": positions[0],
                   "set_m2_target_position": positions[1]}
    post_request(url, aml_request)


def clear_start_motrona_count(request_id, url):
    """ When the motrona counting is active, a gate signal will enable the caen acquisition.
    For this to work, the caen acquisition has to be started aka 'armed' """
    motrona_request = {"request_id": request_id, "clear-start_counting": True}
    post_request(url, motrona_request)


def pause_motrona_count(request_id, url):
    motrona_request = {"request_id": request_id, "pause_counting": True}
    post_request(url, motrona_request)


def motrona_counting_done(url, callback=None):
    if faker:
        time.sleep(faker_time)
        return
    while True:
        time.sleep(1)
        response = http.get_json(url)
        if callback:
            callback(response)
        if response["status"] == "Done":
            logging.info("motrona counting done")
            break


def stop_clear_and_arm_caen_acquisition(request_id, url):
    stop_caen_acquisition(request_id + "_stop", url)
    _clear_caen_acquisition(request_id + "_clear", url)
    _start_caen_acquisition(request_id + "_start", url)


def _start_caen_acquisition(request_id, url):
    request = {'request_id': request_id, 'start': True}
    post_request(url, request)


def _clear_caen_acquisition(request_id, url):
    request = {'request_id': request_id, 'clear': True}
    post_request(url, request)


def stop_caen_acquisition(request_id, url):
    request = {'request_id': request_id, 'stop': True}
    post_request(url, request)


def get_caen_histogram(base_url, board: int, channel: int) -> tuple[Any, List[int]]:
    url = base_url + "/histogram/" + str(board) + "-" + str(channel)
    resp_code, raw_data = http.get_text_with_response_code(url)
    raw_data = raw_data.split(";")
    raw_data.pop()
    data = [int(x) for x in raw_data]
    return resp_code, data


def pack(data: List[int], channel_min, channel_max, channel_width) -> List[int]:
    subset = data[channel_min:channel_max]
    samples_to_group_in_bin = math.floor(len(subset) / channel_width)
    packed_data = []
    for index in range(0, samples_to_group_in_bin * channel_width, samples_to_group_in_bin):
        bin_sum = sum(subset[index:index + samples_to_group_in_bin])
        packed_data.append(bin_sum)
    return packed_data


