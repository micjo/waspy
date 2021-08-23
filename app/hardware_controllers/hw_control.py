import math
from typing import List, Any, Dict

import asyncio
import logging
import app.http_routes.http_helper as http
from app.setup.config import env_conf

logging.basicConfig(level=logging.INFO, filename="debug.log")

faker_time = 0.2


async def wait_for_request_done(url, request):
    if env_conf.FAKER:
        await asyncio.sleep(faker_time)
        return
    while True:
        await asyncio.sleep(0.2)
        response = await http.get_json(url)
        error_message = response["error"]
        if error_message == "Success" or error_message == "No error":
            if response['request_finished'] and response["request_id"] == str(request["request_id"]):
                break
        else:
            raise Exception(url + ": " + error_message)


async def post_request(url, request):
    logging.info("post to: " + url + ", content: " + str(request))
    if env_conf.FAKER:
        await asyncio.sleep(faker_time)
        return

    await http.post_dictionary(url, request)
    await wait_for_request_done(url, request)


async def set_motrona_target_charge(request_id, url, target_charge):
    motrona_request = {"request_id": request_id, "target_charge": target_charge}
    await post_request(url, motrona_request)


async def move_aml_first(request_id, url, position):
    aml_request = {"request_id": request_id, "set_m1_target_position": position}
    await post_request(url, aml_request)


async def move_aml_second(request_id, url, position):
    aml_request = {"request_id": request_id, "set_m2_target_position": position}
    await post_request(url, aml_request)


async def move_aml_both(request_id, url, positions):
    aml_request = {"request_id": request_id, "set_m1_target_position": positions[0],
                   "set_m2_target_position": positions[1]}
    await post_request(url, aml_request)


async def clear_start_motrona_count(request_id, url):
    """ When the motrona counting is active, a gate signal will enable the caen acquisition.
    For this to work, the caen acquisition has to be started aka 'armed' """
    motrona_request = {"request_id": request_id, "clear-start_counting": True}
    await post_request(url, motrona_request)


async def pause_motrona_count(request_id, url):
    motrona_request = {"request_id": request_id, "pause_counting": True}
    await post_request(url, motrona_request)


async def motrona_counting_done(url, callback=None):
    if env_conf.FAKER:
        await asyncio.sleep(faker_time)
        return
    while True:
        await asyncio.sleep(1)
        response = await http.get_json(url)
        if callback:
            callback(response)
        if response["status"] == "Done":
            logging.info("motrona counting done")
            break


async def stop_clear_and_arm_caen_acquisition(request_id, url):
    request = {'request_id': request_id, 'stop_acquisition': True, 'clear': True, 'start_acquisition': True}
    await http.post_dictionary(url, request)
    await wait_for_request_done(url, request)


async def stop_caen_acquisition(request_id, url):
    request = {'request_id': request_id, 'stop_acquisition': True}
    await post_request(url, request)


async def get_caen_histogram(base_url, board: int, channel: int) -> tuple[Any, List[int]]:
    url = base_url + "/histogram/" + str(board) + "-" + str(channel)
    resp_code, raw_data = await http.get_text_with_response_code(url)
    raw_data = raw_data.split(";")
    raw_data.pop()
    data = [int(x) for x in raw_data]
    return resp_code, data


async def get_json_status(url):
    resp_code, data = await http.get_json(url)
    return resp_code, data


def pack(data: List[int], channel_min, channel_max, channel_width) -> List[int]:
    subset = data[channel_min:channel_max]
    samples_to_group_in_bin = math.floor(len(subset) / channel_width)
    packed_data = []
    for index in range(0, samples_to_group_in_bin * channel_width, samples_to_group_in_bin):
        bin_sum = sum(subset[index:index + samples_to_group_in_bin])
        packed_data.append(bin_sum)
    return packed_data


