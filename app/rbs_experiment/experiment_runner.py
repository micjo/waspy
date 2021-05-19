#!/bin/python

import time
import threading
import app.hardware_controllers.data_dump as data_dump

def get_phi_range(full_experiment):
    phi_step = full_experiment["phi_step"]
    phi_start = full_experiment["phi_start"]
    phi_end = full_experiment["phi_end"]
    return list(range(phi_start, phi_end+phi_step, phi_step))

class RbsRunner:
    def __init__(self, config):
        print("lab experiment init")
        self._config = config
        self._running = False
        self.error = ""
        self.lock = threading.Lock()
        self._status = {"status" : "idle"}

    def _safe_update(self, container, key, value):
        with self.lock:
            container[key] = value

    def _start_caen_and_motrona(self, title, motrona_limit):
        comm.pause_motrona_count(title +"_pause", self._config["motrona_rbs"])
        comm.set_motrona_target_charge(title + "_charge", self._config["motrona_rbs"], motrona_limit)
        comm.start_caen_acquisition(title, self._config["caen_charles_evans"])

    def _try_go_into_running_state(self, full_experiment):
        with self.lock:
            if self._running:
                return False
            self._running = True
            self._status = full_experiment
            for scene in full_experiment["experiment"]:
                scene["execution_state"] = "Scheduled"
            self._status["status"] = "Executing"
            return True

    def _run_scene(self, scene, phi_range, storage):
        self._safe_update(scene, "execution_state", "Executing")
        comm.move_aml_both(scene["ftitle"], self._config["aml_x_y"], [ scene["x"], scene["y"] ])

        start = time.time()
        for phi in phi_range:
            title = scene["ftitle"] + "_phi_" + str(phi)
            comm.move_aml_first(title, self._config["aml_phi_zeta"], phi)
            comm.clear_start_motrona_count(title, self._config["motrona_rbs"])
            comm.wait_for_motrona_counting_done(title, self._config["motrona_rbs"])
            self._safe_update(scene, "phi_progress_percentage", round(phi/phi_range[-1]*100,2))
        end = time.time()

        self._safe_update(scene, "measuring_time(sec)", str(round(end-start, 3)))
        data_dump.store_and_plot_histograms(self._config, storage, scene)
        self._safe_update(scene, "execution_state", "Done")


    def _go_to_parking_position(self, title, end_position):
        self._safe_update(self._status, "status", "Moving to end position")
        x_y_end = [end_position["x"], end_position["y"]]
        phi_zeta_end = [end_position["phi"], end_position["zeta"]]
        det_theta_end = [end_position["det"], end_position["theta"]]

        comm.move_aml_both(title + "_end", self._config["aml_x_y"], x_y_end)
        comm.move_aml_both(title + "_end", self._config["aml_phi_zeta"], phi_zeta_end)
        comm.move_aml_both(title + "_end", self._config["aml_det_theta"], det_theta_end)

    def _wrap_up(self):
        with self.lock:
            self._status["status"] = "idle"
            self._running = False

    def run(self, full_experiment):
        print("run called")

        if (not self._try_go_into_running_state(full_experiment)):
            print("Cannot go into running State. Is an experiment already running?")
            return

        title = full_experiment["title"]

        self._start_caen_and_motrona(title, full_experiment["limit"])
        storage = full_experiment["storage"] + "/" + full_experiment["title"]
        phi_range = get_phi_range(full_experiment)

        for scene in full_experiment["experiment"]:
            self._run_scene(scene, phi_range, storage)

        self._go_to_parking_position(title, full_experiment["end_position"])
        self._wrap_up()

    def run_in_background(self, experiment):
        if self._get_running_state():
            print("Experiment ongoing - ignored request")
            return "Experiment ongoing - ignored request"

        task = threading.Thread(target=self.run, args =(experiment,))
        task.start()
        return "Experiment launched in background"

    def _get_running_state(self):
        with self.lock:
            return self._running

    def get_status(self):
        with self.lock:
            return self._status


