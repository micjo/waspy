import asyncio
from pathlib import Path
import logging

import config
from app.rbs_experiment.entities import RbsModel,SceneModel,CaenDetectorModel, StatusModel, empty_experiment
import app.hardware_controllers.daemon_comm as comm
import time
import app.rbs_experiment.entities as entities
import traceback
from app.hardware_controllers.data_dump import store_and_plot_histograms
from typing import List
from config import daemons, dir_config

logging.basicConfig(level=logging.INFO, filename="debug.log")


def _pick_first_file_from_path(path):
    files = [file for file in path.iterdir() if file.is_file()]
    try:
        return files[0]
    except:
        return ""


def _make_folders():
    Path.mkdir(Path(dir_config.watch_dir) , exist_ok=True)
    Path.mkdir(Path(dir_config.ongoing_dir), exist_ok=True)
    Path.mkdir(Path(dir_config.done_dir), exist_ok=True)
    Path.mkdir(Path(dir_config.failed_dir), exist_ok=True)
    Path.mkdir(Path(dir_config.data_dir), exist_ok=True)


def get_phi_range(full_experiment):
    phi_step = full_experiment.phi_step
    phi_start = full_experiment.phi_start
    phi_end = full_experiment.phi_end
    return list(range(phi_start, phi_end+phi_step, phi_step))


def _move_to_folder(file, folder_path):
    file.rename(folder_path / file.name)
    return folder_path / file.name


class RbsExperiment:
    def __init__(self):
        self.run = False
        self.state = entities.ExperimentStateModel(status=StatusModel.Idle,
                experiment= empty_experiment)
        self.experiment_routine = None
        _make_folders()

    def get_state(self):
        return self.state.dict()

    def abort(self):
        self.state.status = StatusModel.Idle
        self.state.experiment = empty_experiment
        self.experiment_routine.cancel()

    async def run_main(self):
        while True:
            await asyncio.sleep(1)
            print("checking folder : " + dir_config.watch_dir )
            f = _pick_first_file_from_path(Path(dir_config.watch_dir))
            if(f):
                try:
                    # todo: copy ongoing file to remote dir - this is an unstable connection
                    f = _move_to_folder(f, Path(dir_config.ongoing_dir))
                    experiment = RbsModel.parse_file(f)
                    self.experiment_routine = asyncio.create_task(self._run_experiment(experiment))
                    await self.experiment_routine
                    _move_to_folder(f, Path(dir_config.done_dir))
                except:
                    _move_to_folder(f, Path(dir_config.failed_dir))
                    print(traceback.format_exc())
                    logging.error(traceback.format_exc())

# rename scene to recipe
    async def _run_scene(self, scene: SceneModel, detectors: List[CaenDetectorModel], phi_range, locations):
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

        #store_plot_histogram is slow and CPU bound -> run in background thread
        await asyncio.get_event_loop().run_in_executor(None,
                store_and_plot_histograms, locations, scene, detectors)
        end = time.time()
        scene.measuring_time_msec = str(round(end-start, 3))
        scene.execution_state = "Done"

    async def _run_experiment(self, experiment: RbsModel):
        self.state.status = StatusModel.Running
        self.state.experiment = experiment
        title = experiment.rqm_number

        charge_limit = experiment.limit
        await comm.pause_motrona_count(title + "_pause", daemons.motrona_rbs.url)
        await comm.set_motrona_target_charge(title + "_charge", daemons.motrona_rbs.url, charge_limit)
        phi_range = get_phi_range(experiment)

        ##TODO: add remote directory here
        locations_with_subfolder = [ dir_config.data_dir + "/" + experiment.rqm_number]

        for scene in experiment.scenario:
            await self._run_scene(scene, experiment.detectors,  phi_range, locations_with_subfolder)

        self.state.status = StatusModel.Parking

        end = experiment.end_position
        await comm.move_aml_both(title + "_end", daemons.aml_x_y.url, [end.x, end.y])
        await comm.move_aml_both(title + "_end", daemons.aml_phi_zeta.url, [end.phi, end.zeta])
        await comm.move_aml_both(title + "_end", daemons.aml_det_theta.url, [end.det, end.theta])

        self.state.status = StatusModel.Idle
