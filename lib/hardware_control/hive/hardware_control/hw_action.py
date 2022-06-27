import math
from typing import List, Any

import logging
import time
from hive.hardware_control import http_helper as http
from hive.hardware_control.rbs_entities import CaenDetector
from hive_exception import HiveError


def set_motrona_target_charge(request_id, url, target_charge):
    motrona_request = {"request_id": request_id, "target_charge": target_charge}
    http.post_request(url, motrona_request)


def move_aml_first(request_id, url, position):
    aml_request = {"request_id": request_id, "set_m1_target_position": position}
    http.post_request(url, aml_request)


def move_aml_second(request_id, url, position):
    aml_request = {"request_id": request_id, "set_m2_target_position": position}
    http.post_request(url, aml_request)


def move_aml_both(request_id, url, positions):
    aml_request = {"request_id": request_id, "set_m1_target_position": positions[0],
                   "set_m2_target_position": positions[1]}
    http.post_request(url, aml_request)


def clear_start_motrona_count(request_id, url):
    """ When the motrona counting is active, a gate signal will enable the caen acquisition.
    For this to work, the caen acquisition has to be started aka 'armed' """
    motrona_request = {"request_id": request_id, "clear-start_counting": True}
    http.post_request(url, motrona_request)


def pause_motrona_count(request_id, url):
    motrona_request = {"request_id": request_id, "pause_counting": True}
    http.post_request(url, motrona_request)


def motrona_counting_done(url):
    while True:
        time.sleep(1)
        response = http.get_json(url)
        if response["status"] == "Done":
            logging.info("motrona counting done")
            break


def stop_clear_and_arm_caen_acquisition(request_id, url):
    stop_caen_acquisition(request_id + "_stop", url)
    _clear_caen_acquisition(request_id + "_clear", url)
    _start_caen_acquisition(request_id + "_start", url)


def caen_read_single_register(request_id: str, url:str, board_id:str, hex_register_address:str):
    request = {
        "request_id": request_id,
        "read_register": {
            "board_id": board_id,
            "register_address": hex_register_address
        }
    }
    http.post_request(url, request)


def caen_set_registry(request_id: str, url: str, board_id: str, registry_filename: str):
    stop_caen_acquisition(request_id + "_stop", url)
    request = {
        "request_id": request_id,
        "upload_registry": {
            "board_id": board_id,
            "filename": registry_filename
        }
    }
    http.post_request(url, request)


def load_aml(request_id, url):
    request = {'request_id': request_id, 'm1_load': True, 'm2_load': True}
    http.post_request(url, request)


def load_mdrive(request_id, url):
    request = {'request_id': request_id, 'load': True}
    http.post_request(url, request)


def _start_caen_acquisition(request_id, url):
    request = {'request_id': request_id, 'start': True}
    http.post_request(url, request)


def _clear_caen_acquisition(request_id, url):
    request = {'request_id': request_id, 'clear': True}
    http.post_request(url, request)


def stop_caen_acquisition(request_id, url):
    request = {'request_id': request_id, 'stop': True}
    http.post_request(url, request)


def get_packed_histogram(base_url, detector: CaenDetector):
    resp_code, data = get_caen_histogram(base_url, detector.board, detector.channel)
    packed_data = pack(data, detector.bins_min, detector.bins_max, detector.bins_width)
    return resp_code, packed_data


def get_caen_histogram(base_url, board: str, channel: int) -> tuple[Any, List[int]]:
    url = base_url + "/histogram/" + str(board) + "/" + str(channel)
    resp_code, raw_data = http.get_text_with_response_code(url)
    if resp_code == 404:
        raise HiveError("Could not retrieve histogram. Does this detector: ({},{}) exist?".format(board, channel))
    raw_data = raw_data.split(";")
    raw_data.pop()
    data = [int(x) for x in raw_data]
    return resp_code, data


def format_caen_histogram(data: List[int]):
    index = 0
    data_string = ""
    for energy_level in data:
        data_string += str(index) + ", " + str(energy_level) + "\n"
        index += 1
    return data_string


def pack(data: List[int], channel_min, channel_max, channel_width) -> List[int]:
    subset = data[channel_min:channel_max]
    samples_to_group_in_bin = math.floor(len(subset) / channel_width)
    packed_data = []
    for index in range(0, samples_to_group_in_bin * channel_width, samples_to_group_in_bin):
        bin_sum = sum(subset[index:index + samples_to_group_in_bin])
        packed_data.append(bin_sum)
    return packed_data


def move_mdrive(request_id, url: str, position: float):
    mdrive_request = {"request_id": request_id, "set_motor_target_position": position}
    http.post_request(url, mdrive_request)


def move_mdrive_done(url):
    while True:
        time.sleep(1)
        response = http.get_json(url)
        if not response["moving_to_target"]:
            logging.info("Motor '" + url + "' has arrived ")
            break


def acquisition_done(url):
    while True:
        time.sleep(1)
        response = http.get_json(url)
        if not response["acquisition_status"]["acquiring"]:
            logging.info("Acquisition has completed")
            break


def acquisition_started(url):
    while True:
        time.sleep(1)
        response = http.get_json(url)
        if response["acquisition_status"]["acquiring"]:
            logging.info("Acquisition has started")
            break
