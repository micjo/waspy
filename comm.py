#!/bin/python

import requests
import time
import sys
import os
import errno
import logging

logging.basicConfig(filename='comm.log', encoding='utf-8', level=logging.DEBUG)

def send_request_and_wait(url, request):
    logging.info("post to: " + url + ", content: " + str(request))
    requests.post(url, json=request)
    while True:
        time.sleep(1)
        response = requests.get(url).json()
        print(response)
        if (response['request_finished'] and response["request_id"] == request["request_id"]):
            break

def set_motrona_target_charge(id, url, target_charge):
    motrona_request = {}
    motrona_request["request_id"] = id
    motrona_request["set_target_targe"] = target_charge
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

def store_caen_histogram(url, location, board, channel):
    print("storing histogram")
    filename = location + "_b" + str(board) + "-c" + str(channel) + ".txt"
    if not os.path.exists(os.path.dirname(filename)):
        try:
            os.makedirs(os.path.dirname(filename))
        except OSError as exc: # Guard against race condition
            if exc.errno != errno.EEXIST:
                raise

    resp = requests.get(url + "/histogram/" + str(board) + "-" + str(channel))
    logging.info("storing histogram of board: " + str(board) + ", channel: " + str(channel) + " to " + filename)
    with open(filename, 'w+') as file:
        file.write(resp.text)


#### OLD STUFF BELOW ####
def wait_for_request_complete(id, currentUrl):
    while True:
        time.sleep(1)
        response = requests.get(currentUrl).json()
        if (response["request_finished"] and response["request_id"] == id):
            print("request " + id + " received")
            return

def move_aml_and_wait(position, id):
    data = { "request_id" : id,
            "set_m1_target_position" : position}
    requests.post(aml_url, json=data)
    wait_for_request_complete(id, aml_url)


def clear_start_counting_and_wait_for_motrona_done(id):
    upId = "clear-start-request_"+str(id)
    data = {"request_id" : upId,
            "clear-start_counting":True}

    requests.post(motrona_url, json=data)
    wait_for_request_complete(upId, motrona_url)

    while True:
        time.sleep(1)
        response = requests.get(motrona_url).json()
        if (response["status"] == "Done"):
            print("motrona counting done")
            break


def finish_caen_acquisition(id):
    requests.post(caen_url, json={
        "request_id" : "finish_" + id,
        "stop_acquisition":True,
        "clear":True
        })
    wait_for_request_complete("finish_" + id, caen_url)
