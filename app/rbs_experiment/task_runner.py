from pathlib import Path
from shutil import copy2
import asyncio
import logging
import traceback

from app.setup.config import cfg
import app.rbs_experiment.entities as rbs
import app.rbs_experiment.recipes as rbs_run


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


class TaskRunner:
    def __init__(self):
        self.dir_scan_paused = False
        self.experiment_routine = None
        self.rbs_status = rbs.RbsRqmStatus(run_status=rbs.StatusModel.Idle, rqm=rbs.empty_rbs_rqm,
                                           active_recipe="", recipe_progress_percentage=0, accumulated_charge=0,
                                           accumulated_charge_target=0)
        _make_folders()

    def get_state(self):
        rbs_state = self.rbs_status.dict()
        rbs_state["dir_scan_paused"] = self.dir_scan_paused
        return rbs_state

    def abort(self):
        self.experiment_routine.cancel()
        self.rbs_status = rbs.RbsRqmStatus(run_status=rbs.StatusModel.Idle, rqm=rbs.empty_rbs_rqm,
                                           active_recipe="", recipe_progress_percentage=0, accumulated_charge=0,
                                           accumulated_charge_target=0)

    async def run_main(self):
        while True:
            await asyncio.sleep(1)
            if self.dir_scan_paused:
                continue

            f = _pick_first_file_from_path(cfg.input_dir.watch)
            if f:
                try:
                    f = move_and_try_copy(f, cfg.output_dir.ongoing, cfg.output_dir_remote.ongoing)
                    experiment = rbs.RbsRqm.parse_file(f)
                    self.experiment_routine = asyncio.create_task(rbs_run.run_recipe_list(experiment, self.rbs_status))
                    await self.experiment_routine
                    move_and_try_copy(f, cfg.output_dir.done, cfg.output_dir_remote.done)
                except:
                    move_and_try_copy(f, cfg.output_dir.failed, cfg.output_dir_remote.failed)
                    logging.error(traceback.format_exc())

    def pause_dir_scan(self, pause):
        self.dir_scan_paused = pause


scanner = TaskRunner()