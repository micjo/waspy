import config, asyncio
from pathlib import Path
from config import urls
import logging
from app.rbs_experiment.entities import RbsModel,SceneModel,CaenDetectorModel
import app.rbs_experiment.daemon_comm as comm
import time
import app.rbs_experiment.entities as entities
import traceback
from app.hardware_controllers.data_dump import store_and_plot_histograms
from typing import List

logging.basicConfig(level=logging.INFO)


def _pick_first_file_from_path(path):
    scan_path = Path(path)
    files = [path for path in scan_path.iterdir() if path.is_file()]
    try:
        return files[0]
    except:
        return ""
        # experiment = ""
        # try:
            # experiment = RbsModel.parse_file(f)
            # f.rename(f.parent / "ongoing" / f.name)
            # logging.info("New experiment scheduled: " + str(experiment.json()))
        # except Exception as exc:
            # f.rename(f.parent / "failed" / f.name)
            # logging.error(exc)
        # return experiment

def _make_folders(path):
    Path.mkdir(Path(path), exist_ok=True)
    Path.mkdir(Path(path) / "ongoing", exist_ok=True)
    Path.mkdir(Path(path) / "done", exist_ok=True)
    Path.mkdir(Path(path) / "failed", exist_ok=True)

def get_phi_range(full_experiment):
    phi_step = full_experiment.phi_step
    phi_start = full_experiment.phi_start
    phi_end = full_experiment.phi_end
    return list(range(phi_start, phi_end+phi_step, phi_step))

def _move_to_folder(file, folderPath):
    file.rename(file.parent / folderPath / file.name)
    return file.parent / folderPath / file.name

class RbsExperiment:
    def __init__(self):
        self.run = False
        self.status = entities.ExperimentStatusModel()
        self.experiment_routine = None
        _make_folders(config.watch_dir)

    def abort(self):
        self.experiment_routine.cancel()

    async def run_main(self):
        while True:
            await asyncio.sleep(1)
            f = _pick_first_file_from_path(config.watch_dir)
            if(f):
                try:
                    f = _move_to_folder(f, "ongoing")
                    experiment = RbsModel.parse_file(f)
                    self.experiment_routine = asyncio.create_task(self._run_experiment(experiment))
                    await self.experiment_routine
                    _move_to_folder(f, "../done")
                except:
                    _move_to_folder(f, "../failed")
                    traceback.print_exc()

    async def _run_scene(self, scene: SceneModel, detectors: List[CaenDetectorModel], phi_range, storage_folder):
        scene.execution_state = "Executing"
        start = time.time()
        await comm.move_aml_both(scene.ftitle, urls.aml_x_y, [scene.x, scene.y])
        await comm.clear_and_arm_caen_acquisition(scene.ftitle, urls.caen_charles_evans)

        scene.phi_progress = 0
        for phi in phi_range:
            title = scene.ftitle + "_phi_" + str(phi)
            await comm.move_aml_first(title, urls.aml_phi_zeta, phi)
            await comm.clear_start_motrona_count(title, urls.motrona_rbs)
            await comm.motrona_counting_done(urls.motrona_rbs)
            scene.phi_progress = round (phi/phi_range[-1]) * 100

        #store_plot_histogram is slow and CPU bound -> run in background thread
        await asyncio.get_event_loop().run_in_executor(None,
                store_and_plot_histograms, storage_folder, scene, detectors)

        end = time.time()
        scene.measuring_time_msec = str(round(end-start, 3))
        scene.execution_state = "Done"

    async def _run_experiment(self, experiment: RbsModel):
        self.status.state = "Running"
        self.status.experiment = experiment
        title = experiment.title

        charge_limit = experiment.limit
        await comm.pause_motrona_count(title + "_pause", urls.motrona_rbs)
        await comm.set_motrona_target_charge(title + "_charge", urls.motrona_rbs, charge_limit)
        phi_range = get_phi_range(experiment)
        storage_folder = Path(experiment.storage) / Path(experiment.title)

        for scene in experiment.scenario:
            await self._run_scene(scene, experiment.detectors,  phi_range, storage_folder)

        end = experiment.end_position
        await comm.move_aml_both(title + "_end", urls.aml_x_y, [end.x, end.y])
        await comm.move_aml_both(title + "_end", urls.aml_phi_zeta, [end.phi, end.zeta])
        await comm.move_aml_both(title + "_end", urls.aml_det_theta, [end.det, end.theta])

        self.status.state = "Idle"
