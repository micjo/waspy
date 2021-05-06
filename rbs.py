#!/bin/python

import logging
import requests
import time
import sys
import comm
import json
import threading


aml_x_y_url = 'http://127.0.0.1:5000/api/aml_x_y'
aml_phi_zeta_url = 'http://127.0.0.1:5000/api/aml_phi_zeta'
aml_det_theta_url = 'http://127.0.0.1:5000/api/aml_det_theta'
motrona_url = 'http://127.0.0.1:5000/api/motrona_rbs'
caen_url = 'http://127.0.0.1:5000/api/caen_charles_evans'

def get_phi_range(full_experiment):
    phi_step = full_experiment["phi_step"]
    phi_start = full_experiment["phi_start"]
    phi_end = full_experiment["phi_end"]
    return list(range(phi_start, phi_end+phi_step, phi_step))

def run_rbs_experiment(config, full_experiment):
    storage = full_experiment["storage"]
    phi_range = get_phi_range(full_experiment)
    title = full_experiment["title"]
    motrona_limit = full_experiment["limit"]

    comm.pause_motrona_count(title)
    comm.set_motrona_target_charge(title, motrona_limit)
    comm.start_caen_acquisition(title)

    for scene in full_experiment["experiment"]:
        scene_title = scene["ftitle"]
        scene_file = scene["file"]
        x_target = scene["x"]
        y_target = scene["y"]
        comm.move_aml_both(scene_title, config["aml_x_y"], [x_target, y_target])
        for phi in phi_range:
            title = scene_title + "_phi_" +str(phi)
            comm.move_aml_first(title, config["aml_phi_zeta"], phi)
            comm.clear_start_motrona_count(title)
            comm.wait_for_motrona_counting_done(title)
        comm.store_caen_histogram(storage + "/" + scene_file, 0, 0)

    end_position = full_experiment["end_position"]
    x_y_end = [end_position["x"], end_position["y"]]
    phi_zeta_end = [end_position["phi"], end_position["zeta"]]
    det_theta_end = [end_position["det"], end_position["theta"]]

    comm.move_aml_both(title + "_end", config["aml_x_y"], x_y_end)
    comm.move_aml_both(title + "_end", config["aml_phi_zeta"], phi_zeta_end)
    comm.move_aml_both(title + "_end", config["aml_det_theta"], det_theta_end)

class RbsRunner:
    def __init__(self, config):
        print("lab experiment init")
        self.config = config
        self.__running = False
        self.error = ""
        self.lock = threading.Lock()
        self.__status = {}

    def run(self, full_experiment):
        with self.lock:
            self.__running = True
            self.__status = full_experiment

        storage = full_experiment["storage"]
        phi_range = get_phi_range(full_experiment)
        title = full_experiment["title"]
        motrona_limit = full_experiment["limit"]

        comm.pause_motrona_count(title, self.config["motrona_rbs"])
        comm.set_motrona_target_charge(title, self.config["motrona_rbs"], motrona_limit)
        comm.start_caen_acquisition(title, self.config["caen_charles_evans"])

        for scene in full_experiment["experiment"]:
            scene_title = scene["ftitle"]
            scene_file = scene["file"]
            x_target = scene["x"]
            y_target = scene["y"]
            comm.move_aml_both(scene_title, self.config["aml_x_y"], [x_target, y_target])
            for phi in phi_range:
                title = scene_title + "_phi_" +str(phi)
                comm.move_aml_first(title, self.config["aml_phi_zeta"], phi)
                comm.clear_start_motrona_count(title, self.config["motrona_rbs"])
                comm.wait_for_motrona_counting_done(self.config["motrona_rbs"], title)
            comm.store_caen_histogram(self.config["caen_charles_evans"], storage + "/" + scene_file, 0, 0)

        end_position = full_experiment["end_position"]
        x_y_end = [end_position["x"], end_position["y"]]
        phi_zeta_end = [end_position["phi"], end_position["zeta"]]
        det_theta_end = [end_position["det"], end_position["theta"]]

        comm.move_aml_both(title + "_end", self.config["aml_x_y"], x_y_end)
        comm.move_aml_both(title + "_end", self.config["aml_phi_zeta"], phi_zeta_end)
        comm.move_aml_both(title + "_end", self.config["aml_det_theta"], det_theta_end)

    def run_in_background(self, experiment):
        if self.__get_running_state():
            print("Experiment ongoing - ignored request")
            return "Experiment ongoing - ignored request"

        task = threading.Thread(target=self.run, args =(experiment,))
        task.start()
        return "Experiment launched in background"

    def __get_experiment_status(self):
        ret_val = ""
        with self.lock:
            ret_val = self.__status
        return ret_val

    def __set_running_state(self, state):
        with self.lock:
            self.__running = state

    def __get_running_state(self):
        ret_val = True
        with self.lock:
            ret_val = self.__running
        return ret_val

    def get_status(self):
        with self.lock:
            return status
