from fastapi import APIRouter
import config, asyncio, json
from pathlib import Path
import config


def _read_json_from_file(file_path):
    with open(file_path) as watch_file:
        content = watch_file.read()
        try:
            json_exp = json.loads(content)
            return json_exp
        except Exception as err:
            print(err)

def _check_folder(path):
    scan_path = Path(path)
    files = [path for path in scan_path.iterdir() if path.is_file()]
    for f in files:
        experiment = _read_json_from_file(f)
        return experiment


class RbsExperiment:

    def __init__(self):
        self.run = False
        self.status = {"idle": True}
        Path.mkdir(Path(config.watch_dir) / "ongoing", exist_ok=True)
        Path.mkdir(Path(config.watch_dir) / "done", exist_ok=True)
        Path.mkdir(Path(config.watch_dir) / "failed", exist_ok=True)

    async def run_main(self):
        while True:
            await asyncio.sleep(1)
            experiment = _check_folder(config.watch_dir)
            if (experiment):
                print("scheduling experiment")


router = APIRouter()



