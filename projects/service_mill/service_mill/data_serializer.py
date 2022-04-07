import traceback
from datetime import datetime
from pathlib import Path
from shutil import move, copy2
from typing import Dict

from erd_entities import DoublePath
import io
import logging
import pandas as pd
import json


class DataSerializer:
    _root_dir: DoublePath
    _base_folder: Path
    _sub_folder: Path

    def __init__(self, data_dir):
        self._root_dir = data_dir
        self._sub_folder = ""
        self._make_folders()

    def set_base_folder(self, folder: str):
        self._base_folder = Path(folder)
        self._sub_folder = Path("")
        Path.mkdir(self._root_dir.local / self._base_folder, exist_ok=True)
        Path.mkdir(self._root_dir.remote / self._base_folder, exist_ok=True)
        subdir = "old_" + datetime.now().strftime("%Y-%m-%d_%H.%M.%S")
        self._move_files(self._root_dir.local, subdir)
        self._move_files(self._root_dir.remote, subdir)

    def set_sub_folder(self, folder:str):
        self._sub_folder = Path(folder)
        Path.mkdir(self._root_dir.local / self._base_folder / self._sub_folder, exist_ok=True)
        Path.mkdir(self._root_dir.remote / self._base_folder / self._sub_folder, exist_ok=True)

    def write_bytes_to_disk(self, filename: str, content: io.BytesIO):
        content.seek(0)
        with open(self._in_local_path(filename), "wb") as f:
            f.write(content.getbuffer().tobytes())
        _try_copy(self._in_local_path(filename), self._in_remote_path(filename))
        content.close()

    def write_text_to_disk(self, filename: str, content:str):
        with open(self._in_local_path(filename), 'w+') as f:
            f.write(content)
        _try_copy(self._in_local_path(filename), self._in_remote_path(filename))

    def write_csv_panda_to_disk(self, filename: str, content: Dict):
        df = pd.DataFrame.from_dict(content)
        self.write_text_to_disk(filename, df.to_csv(index=False))

    def write_json_to_disk(self, filename, content: Dict):
        json_content = json.dumps(content, indent=4, default=str)
        self.write_text_to_disk(filename, json_content)

    def _in_local_path(self, file_stem: str):
        return self._root_dir.local / self._base_folder / self._sub_folder / file_stem

    def _in_remote_path(self, file_stem: str):
        return self._root_dir.remote / self._base_folder / self._sub_folder / file_stem

    def _make_folders(self):
        Path.mkdir(self._root_dir.local, parents=True, exist_ok=True)
        Path.mkdir(self._root_dir.remote, parents=True, exist_ok=True)

    def _move_files(self, base, subdir):
        files_to_move = [x for x in (base / self._base_folder).iterdir() if not x.stem.startswith("old_")]
        if files_to_move:
            full_subdir = base / self._base_folder / subdir
            logging.info("Existing files found, moving them to: '" + str(full_subdir) + "'.")
            Path.mkdir(full_subdir, exist_ok=True)
            for file in files_to_move:
                move(file, full_subdir)


def _try_copy(source, destination):
    logging.info("copying {source} to {destination}".format(source=source, destination=destination))
    try:
        Path.mkdir(destination.parent, exist_ok=True)
        copy2(source, destination)
    except:
        logging.error(traceback.format_exc())
