from app.config.config import daemons, input_dir, output_dir, output_dir_remote
from app.hardware_controllers.data_dump import store_and_plot_histograms
from app.rbs_experiment.entities import RbsModel,RecipeInstruction,CaenDetectorModel, StatusModel, empty_experiment, PositionModel
from pathlib import Path
from shutil import copy2
from typing import List
import app.hardware_controllers.daemon_comm as comm
import app.rbs_experiment.entities as entities
import asyncio
import logging
import time
import traceback

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


def get_phi_range(full_experiment):
    phi_step = full_experiment.phi_step
    phi_start = full_experiment.phi_start
    phi_end = full_experiment.phi_end
    return list(range(phi_start, phi_end+phi_step, phi_step))


def _move_and_try_copy(file, move_folder, copy_folder):
    file.rename(move_folder / file.name)
    file = move_folder / file.name
    try:
        copy2(file, copy_folder)
    except:
        print(traceback.format_exc())
        logging.error(traceback.format_exc())
    return file

async def _move_to_position(title: str, position: PositionModel):
    await comm.move_aml_both(title + "_end", daemons.aml_x_y.url, [position.x, position.y])
    await comm.move_aml_both(title + "_end", daemons.aml_phi_zeta.url, [position.phi, position.zeta])
    await comm.move_aml_both(title + "_end", daemons.aml_det_theta.url, [position.det, position.theta])


class RbsExperiment:
    def __init__(self):
        self.dir_scan_paused = False
        self.state = entities.ExperimentStateModel(status=StatusModel.Idle,
                experiment= empty_experiment)
        self.experiment_routine = None
        _make_folders()

    def get_state(self):
        rbs_state = self.state.dict()
        rbs_state["dir_scan_paused"] = self.dir_scan_paused
        return rbs_state

    def abort(self):
        self.state.status = StatusModel.Idle
        self.state.experiment = empty_experiment
        self.experiment_routine.cancel()

    async def run_main(self):
        while True:
            logging.info("scanning")
            await asyncio.sleep(1)
            if self.dir_scan_paused:
                continue

            f = _pick_first_file_from_path(input_dir.watch)
            if(f):
                try:
                    f = _move_and_try_copy(f, output_dir.ongoing, output_dir_remote.ongoing)
                    experiment = RbsModel.parse_file(f)
                    self.experiment_routine = asyncio.create_task(self._run_experiment(experiment))
                    await self.experiment_routine
                    _move_and_try_copy(f, output_dir.done, output_dir_remote.done)
                except:
                    _move_and_try_copy(f, output_dir.failed, output_dir_remote.failed)
                    print(traceback.format_exc())
                    logging.error(traceback.format_exc())

# rename scene to recipe
    async def _run_scene(self, scene: RecipeInstruction, detectors: List[CaenDetectorModel], phi_range, rqm_number):
        scene.execution_state = "Executing"
        start = time.time()
        await comm.move_aml_both(scene.ftitle, daemons.aml_x_y.url, [scene.x, scene.y])
        await comm.clear_and_arm_caen_acquisition(scene.ftitle, daemons.caen_charles_evans.url)

        scene.phi_progress = "0"
        for phi in phi_range:
            title = scene.ftitle + "_phi_" + str(phi)
            await comm.move_aml_first(title, daemons.aml_phi_zeta.url, phi)
            await comm.clear_start_motrona_count(title, daemons.motrona_rbs.url)
            await comm.motrona_counting_done(daemons.motrona_rbs.url)
            # scene.phi_progress = round(phi/phi_range[-1] * 100,2)

        end = time.time()
        time_delta = (end-start)
        scene.measuring_time_sec = str(round(time_delta, 3))
        #store_plot_histogram is slow and CPU bound -> run in background thread
        await asyncio.get_event_loop().run_in_executor(None, store_and_plot_histograms, rqm_number, scene, detectors)
        scene.execution_state = "Done"

    async def _run_experiment(self, experiment: RbsModel):
        self.state.status = StatusModel.Running
        self.state.experiment = experiment
        title = experiment.rqm_number
        phi_range = get_phi_range(experiment)
        charge_limit = experiment.limit / len(phi_range)
        print(charge_limit)
        await _move_to_position(title + "_start", experiment.starting_position)
        await comm.pause_motrona_count(title + "_pause", daemons.motrona_rbs.url)
        await comm.set_motrona_target_charge(title + "_charge", daemons.motrona_rbs.url, charge_limit)

        for scene in experiment.recipe:
            await self._run_scene(scene, experiment.detectors,  phi_range, experiment.rqm_number)

        self.state.status = StatusModel.Parking
        await _move_to_position(title, experiment.parking_position)

        self.state.status = StatusModel.Idle


    def pause_dir_scan(self, pause):
        self.dir_scan_paused = pause
