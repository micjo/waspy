#!/bin/python

import requests
import time
import sys

aml_url = 'http://127.0.0.1:5000/api/aml_x_y'
motrona_url = 'http://127.0.0.1:5000/api/motrona_rbs'
caen_url = 'http://127.0.0.1:5000/api/caen_charles_evans'


def wait_for_request_complete(id, currentUrl):
    while True:
        time.sleep(1)
        response = requests.get(currentUrl).json()
        if (response["request_finished"] and response["request_id"] == id):
            print("request " + id + " received")
            break



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


def start_caen_acquisition(id):
    print('start acq')
    response = requests.post(caen_url, json={
        "request_id" : "start_" + id,
        "start_acquisition":True
        })
    print(response)

def finish_caen_acquisition(id):
    resp = requests.get(caen_url + "/histogram/1-0")
    with open('data_' +id+ '.txt', 'w') as file:
        file.write(resp.text)
    requests.post(caen_url, json={
        "request_id" : "finish_" + id,
        "stop_acquisition":True,
        "clear":True
        })

def run_rbs_experiment(start,end,step):
    for i in range (start,end,step):
        print(i)
        request_id = "step_" + str(i)
        move_aml_and_wait(i, request_id)
        start_caen_acquisition(request_id)
        clear_start_counting_and_wait_for_motrona_done(request_id)
        finish_caen_acquisition(request_id)
    print("all done")







