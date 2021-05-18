import config, asyncio
from pathlib import Path
from config import direct_urls
import logging
from app.rbs_experiment.entities import RbsSchema,SceneModel
import app.rbs_experiment.daemon_comm as comm
import time

logging.basicConfig(level=logging.INFO)

def _check_folder(path):
    scan_path = Path(path)
    files = [path for path in scan_path.iterdir() if path.is_file()]
    for f in files:
        experiment = ""
        try:
            experiment = RbsSchema.parse_file(f)
            f.rename(f.parent / "ongoing" / f.name)
            logging.info("New experiment scheduled: " + str(experiment.json()))
        except Exception as exc:
            f.rename(f.parent / "failed" / f.name)
            logging.error(exc)
        return experiment

def _make_folders(path):
    Path.mkdir(Path(path), exist_ok=True)
    Path.mkdir(Path(path) / "ongoing", exist_ok=True)
    Path.mkdir(Path(path) / "done", exist_ok=True)
    Path.mkdir(Path(path) / "failed", exist_ok=True)
    Path.mkdir(Path(path) / "failed", exist_ok=True)

def get_phi_range(full_experiment):
    phi_step = full_experiment.phi_step
    phi_start = full_experiment.phi_start
    phi_end = full_experiment.phi_end
    return list(range(phi_start, phi_end+phi_step, phi_step))

class RbsExperiment:
    def __init__(self):
        self.run = False
        self.status = {"idle": True, "experiment":{}}
        _make_folders(config.watch_dir)

    async def run_main(self):
        while True:
            await asyncio.sleep(1)
            experiment = _check_folder(config.watch_dir)
            if (experiment):
                try:
                    await self._run_experiment(experiment)
                except Exception as exc:
                    print("Something went wrong during the experiment: " + str(exc))


    async def _run_scene(self, scene: SceneModel, phi_range, storage_folder):
        scene.execution_state = "Executing"
        await comm.move_aml_both(scene.ftitle, direct_urls.aml_x_y, [scene.x, scene.y])
        start = time.time()

        scene.phi_progress = 0
        for phi in phi_range:
            title = scene.ftitle + "_phi_" + str(phi)
            await comm.move_aml_first(title, direct_urls.aml_phi_zeta, phi)
            await comm.clear_and_arm_caen_acquisition(title, direct_urls.caen_charles_evans)
            await comm.clear_start_motrona_count(title, direct_urls.motrona_rbs)
            await comm.motrona_counting_done(title)
            scene.phi_progress = round (phi/phi_range[-1]) * 100

    async def _run_experiment(self, experiment: RbsSchema):
        self.status["idle"] = False
        self.status["experiment"] = experiment.dict
        title = experiment.title

        charge_limit = experiment.limit
        await comm.pause_motrona_count(title + "_pause", direct_urls.motrona_rbs)
        await comm.set_motrona_target_charge(title + "_charge", direct_urls.motrona_rbs, charge_limit)
        phi_range = get_phi_range(experiment)
        storage_folder = Path(experiment.storage) / Path(experiment.title)

        for scene in experiment.scenario:
            await self._run_scene(scene, phi_range, storage_folder)

        # Path.mkdir(storage)


        self.status["idle"] = True
