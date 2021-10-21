import sys
from pathlib import Path
from shutil import copy2
import logging

from app.rbs_experiment.entities import RbsRqm
from app.rbs_experiment.recipe_list_runner import RecipeListRunner
from app.setup.config import cfg
from threading import Thread
import traceback
import time



def _pick_first_file_from_path(path):
    files = [file for file in sorted(path.iterdir()) if file.is_file()]
    try:
        return files[0]
    except:
        return ""


def _make_folders():
    Path.mkdir(cfg.input_dir.watch, parents=True, exist_ok=True)
    Path.mkdir(cfg.output_dir.ongoing, parents=True, exist_ok=True)
    Path.mkdir(cfg.output_dir.done, parents=True, exist_ok=True)
    Path.mkdir(cfg.output_dir.failed, parents=True, exist_ok=True)
    Path.mkdir(cfg.output_dir.data, parents=True, exist_ok=True)


def move_and_try_copy(file, move_folder, copy_folder):
    file.replace(move_folder / file.name)
    file = move_folder / file.name
    try:
        copy2(file, copy_folder)
    except:
        logging.error(traceback.format_exc())
    return file


class RqmDispatcher(Thread):
    def __init__(self, recipe_runner: RecipeListRunner):
        Thread.__init__(self)
        self.dir_scan_paused = False
        self.recipe_runner = recipe_runner
        _make_folders()

    def get_state(self):
        rbs_state = self.rbs_status.dict()
        rbs_state["dir_scan_paused"] = self.dir_scan_paused
        return rbs_state

    def abort(self):
        self.recipe_runner.abort()
        self.recipe_runner.start()

    def run(self):
        self.recipe_runner.start()
        while True:
            time.sleep(1)
            if self.dir_scan_paused:
                continue

            f = _pick_first_file_from_path(cfg.input_dir.watch)
            if f:
                try:
                    f = move_and_try_copy(f, cfg.output_dir.ongoing, cfg.output_dir_remote.ongoing)
                    experiment = RbsRqm.parse_file(f)
                    self.recipe_runner.add_rqm_to_queue(experiment)
                    move_and_try_copy(f, cfg.output_dir.done, cfg.output_dir_remote.done)
                except:
                    move_and_try_copy(f, cfg.output_dir.failed, cfg.output_dir_remote.failed)
                    logging.error(traceback.format_exc())

    def pause_dir_scan(self, pause):
        self.dir_scan_paused = pause


