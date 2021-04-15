#!/bin/python

import requests
import time
import sys

aml_url = 'http://localhost:5000/api/aml_x_y'
motrona_url = 'http://localhost:5000/api/motrona_rbs'


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
    


def run_rbs_experiment(start,end,step):
    for i in range (start,end,step):
        print(i)
        request_id = "step_" + str(i)
        move_aml_and_wait(i, request_id)
        clear_start_counting_and_wait_for_motrona_done(request_id)

    print("all done")

if __name__ == "__main__":
    run_rbs_experiment(int(sys.argv[1]),int(sys.argv[2]),int(sys.argv[3]))








