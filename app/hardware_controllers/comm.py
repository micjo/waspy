#!/bin/python

import requests
import time
import logging

logging.basicConfig(filename='comm.log', level=logging.DEBUG)

def send_request_and_wait(url, request):
    logging.info("post to: " + url + ", content: " + str(request))
    time.sleep(1)
    return
    requests.post(url, json=request)
    while True:
        time.sleep(0.2)
        response = requests.get(url).json()
        if (response['request_finished'] and response["request_id"] == request["request_id"]):
            break


def get_json_status(url):
    return requests.get(url).json()

def set_motrona_target_charge(id, url, target_charge):
    motrona_request = {}
    motrona_request["request_id"] = id
    motrona_request["target_charge"] = target_charge
    send_request_and_wait(url, motrona_request)

def move_aml_first(id, url, position):
    aml_request = {}
    aml_request["request_id"] = id
    aml_request["set_m1_target_position"] = position
    send_request_and_wait(url, aml_request)

def move_aml_second(id, url, position):
    aml_request = {}
    aml_request["request_id"] = id
    aml_request["set_m2_target_position"] = position
    send_request_and_wait(url, aml_request)

def move_aml_both(id, url, positions):
    aml_request = {}
    aml_request["request_id"] = id
    aml_request["set_m1_target_position"] = positions[0]
    aml_request["set_m2_target_position"] = positions[1]
    send_request_and_wait(url, aml_request)

def clear_start_motrona_count(id, url):
    motrona_request = {}
    motrona_request["request_id"] = id
    motrona_request["clear-start_counting"] = True
    send_request_and_wait(url, motrona_request)

def pause_motrona_count(id, url):
    motrona_request = {}
    motrona_request["request_id"] = id
    motrona_request["pause_counting"] = True
    send_request_and_wait(url, motrona_request)

def wait_for_motrona_counting_done(id, url):
    time.sleep(1)
    return
    while True:
        time.sleep(1)
        response = requests.get(url).json()
        if (response["status"] == "Done"):
            logging.info("motrona counting done")
            break

def start_caen_acquisition(id, url):
    request = {}
    request['request_id'] = id
    request['start_acquisition'] = True
    send_request_and_wait(url, request)

