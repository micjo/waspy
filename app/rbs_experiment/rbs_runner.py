from app.setup.config import daemons, input_dir, output_dir, output_dir_remote
from app.hardware_controllers.data_dump import store_and_plot_histograms
from app.rbs_experiment.entities import RbsModel, Recipe, CaenDetectorModel, StatusModel, empty_rqm, PositionModel
from pathlib import Path
from shutil import copy2
from typing import List
import app.hardware_controllers.daemon_comm as comm
import app.rbs_experiment.entities as entities
import asyncio
import logging
import time
import traceback
import app.rbs_experiment.rbs_daemon_control as control
import app.rbs_experiment.entities as rbs



def _pick_first_file_from_path(path):
    files = [file for file in path.iterdir() if file.is_file()]
    try:
        return files[0]
    except:
        return ""


def _make_folders():
    Path.mkdir(input_dir.watch, parents=True, exist_ok=True)
    Path.mkdir(output_dir.ongoing, parents=True, exist_ok=True)
    Path.mkdir(output_dir.done, parents=True, exist_ok=True)
    Path.mkdir(output_dir.failed, parents=True, exist_ok=True)
    Path.mkdir(output_dir.data, parents=True, exist_ok=True)


def _move_and_try_copy(file, move_folder, copy_folder):
    file.rename(move_folder / file.name)
    file = move_folder / file.name
    try:
        copy2(file, copy_folder)
    except:
        print(traceback.format_exc())
        logging.error(traceback.format_exc())
    return file

class RbsRunner:
    def __init__(self):
        self.dir_scan_paused = False
        self.experiment_routine = None
        self.rbs_status = entities.RbsRqmStatus(run_status=StatusModel.Idle, recipe_list=entities.empty_rbs_rqm)
        _make_folders()

    def get_state(self):
        rbs_state = self.rbs_status.dict()
        rbs_state["dir_scan_paused"] = self.dir_scan_paused
        return rbs_state

    def abort(self):
        self.experiment_routine.cancel()
        self.rbs_status = entities.RbsRqmStatus(run_status=StatusModel.Idle, recipe_list=entities.empty_rbs_rqm)

    async def run_main(self):
        while True:
            await asyncio.sleep(1)
            if self.dir_scan_paused:
                continue

            f = _pick_first_file_from_path(input_dir.watch)
            if f:
                try:
                    f = _move_and_try_copy(f, output_dir.ongoing, output_dir_remote.ongoing)
                    experiment = rbs.RbsRqmStatus.parse_file(f)
                    self.experiment_routine = asyncio.create_task(control.run_recipe_list(self.status, experiment))
                    await self.experiment_routine
                    _move_and_try_copy(f, output_dir.done, output_dir_remote.done)
                except:
                    _move_and_try_copy(f, output_dir.failed, output_dir_remote.failed)
                    print(traceback.format_exc())
                    logging.error(traceback.format_exc())

    def pause_dir_scan(self, pause):
        self.dir_scan_paused = pause
