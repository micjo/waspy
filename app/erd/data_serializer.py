import json
import logging
import traceback
from datetime import datetime
from pathlib import Path
from shutil import copy2, move
import copy
from threading import Lock

from app.rbs.entities import DoublePath


def _try_copy(source, destination):
    logging.info("copying {source} to {destination}".format(source=source, destination=destination))
    try:
        Path.mkdir(destination.parent, exist_ok=True)
        copy2(source, destination)
    except:
        logging.error(traceback.format_exc())


class ErdDataSerializer:
    data_dir: DoublePath
    base_folder: Path
    sub_folder: Path

    def __init__(self, data_dir: DoublePath):
        self.data_dir = data_dir
        self.sub_folder = Path("")
        self._make_folders()
        self._lock = Lock()
        self._abort = False

    def abort(self):
        with self._lock:
            self._abort = True

    def resume(self):
        with self._lock:
            self._abort = False

    def aborted(self):
        with self._lock:
            return copy.deepcopy(self._abort)

    def _make_folders(self):
        Path.mkdir(self.data_dir.local, parents=True, exist_ok=True)
        Path.mkdir(self.data_dir.remote, parents=True, exist_ok=True)

    def clear_sub_folder(self):
        self.sub_folder = Path("")

    def set_base_folder(self, base_folder: str):
        self.base_folder = Path(base_folder)
        Path.mkdir(self.data_dir.local / self.base_folder, exist_ok=True)
        Path.mkdir(self.data_dir.remote / self.base_folder, exist_ok=True)
        subdir = "old_" + datetime.now().strftime("%Y-%m-%d_%H.%M.%S")
        self.move_files(self.data_dir.local, subdir)
        self.move_files(self.data_dir.remote, subdir)

    def move_files(self, base, subdir):
        files_to_move = [x for x in (base / self.base_folder).iterdir() if not x.stem.startswith("old_")]
        if files_to_move:
            full_subdir = base / self.base_folder / subdir
            logging.info("Existing files found, moving them to: '" + str(full_subdir) + "'.")
            Path.mkdir(full_subdir, exist_ok=True)
            for file in files_to_move:
                move(file, full_subdir)

    def save_rqm(self, rqm: dict):
        file_stem = "active_rqm.txt"
        local = self.data_dir.local / self._get_folder() / file_stem
        remote = self.data_dir.remote / self._get_folder() / file_stem
        with open(local, 'w+') as f:
            f.write("Running RQM:\n")
            f.write(json.dumps(rqm, indent=4))
        _try_copy(local, remote)

    def set_sub_folder(self, sub_folder: str):
        self.sub_folder = Path(sub_folder)
        Path.mkdir(self.data_dir.remote / self.base_folder / self.sub_folder, exist_ok=True)

    def _get_folder(self):
        return self.base_folder / self.sub_folder

    def save_histogram(self, histogram: str, file_stem):
        if self.aborted():
            return
        file_stem += ".txt"
        local = self.data_dir.local / self._get_folder() / file_stem
        remote = self.data_dir.remote / self._get_folder() / file_stem
        with open(local, 'w+') as f:
            f.write(histogram)
        _try_copy(local, remote)
