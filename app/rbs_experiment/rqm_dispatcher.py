import copy
import queue
import sys
from pathlib import Path
from queue import Queue
from shutil import copy2
import logging
from typing import List

from app.rbs_experiment.entities import RbsRqm, DispatcherConfig
from app.rbs_experiment.recipe_list_runner import RecipeListRunner
from threading import Thread, Lock, Condition
import traceback
import time


def _pick_first_file_from_path(path):
    files = [file for file in sorted(path.iterdir()) if file.is_file()]
    try:
        return files[0]
    except:
        return ""


def move_and_try_copy(file, move_folder, copy_folder):
    file.replace(move_folder / file.name)
    file = move_folder / file.name
    try:
        copy2(file, copy_folder)
    except:
        logging.error(traceback.format_exc())
    return file


class RqmDispatcher(Thread):
    rqms: List[RbsRqm]

    def __init__(self, recipe_runner: RecipeListRunner):
        Thread.__init__(self)
        self.dir_scan_paused = False
        self.recipe_runner = recipe_runner
        self.recipe_runner.daemon = True
        self.lock = Lock()
        self.pause_request = Queue[str]
        self.pause_condition = Condition()
        self.enqueue_rqm = Condition()
        self.rqms = []

    def get_state(self):
        with self.enqueue_rqm:
            rqms = copy.deepcopy(self.rqms)
        rbs_state = {"dir_scan_paused": self.dir_scan_paused, "queue": rqms}
        return rbs_state

    def abort(self):
        self.recipe_runner.abort()
        self.recipe_runner.start()

    def run(self):
        self.recipe_runner.start()
        while True:
            time.sleep(1)
            try:
                self.recipe_runner.rqm_queue.put_nowait(self.get_next_rqm())
                self.clear_next_rqm()
            except queue.Full:
                print("Recipe runner is already busy. back off.")
            except IndexError:
                pass

    def get_next_rqm(self) -> RbsRqm:
        with self.enqueue_rqm:
            return copy.deepcopy(self.rqms[0])

    def clear_next_rqm(self):
        with self.enqueue_rqm:
            self.rqms.pop(0)

    def add_rqm_to_queue(self, rqm: RbsRqm):
        with self.enqueue_rqm:
            self.rqms.append(rqm)
