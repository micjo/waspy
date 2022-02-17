import requests
import time
from datetime import datetime, timedelta
from pathlib import Path
from threading import Lock
from threading import Thread
from typing import Dict, List

import numpy as np
import pandas as pd
from pydantic import BaseModel

from app.hardware_controllers.entities import SimpleConfig
from app.setup.config import HiveConfig, GlobalConfig

env_config = GlobalConfig()
BASE_PATH = Path(env_config.TREND_STORE)


def get_path(today: str, file_stem: str, suffix: int) -> Path:
    return BASE_PATH / "{today}_{file_stem}_{leader:03d}.txt".format(today=today, file_stem=file_stem, leader=suffix)


def get_existing_suffix(today: str, file_stem: str) -> int:
    i = 0
    while get_path(today, file_stem, i).exists():
        i += 1
    return i - 1


def is_trend_file_missing(today: str, file_stem: str, suffix: int) -> bool:
    full_path = get_path(today, file_stem, suffix)
    return not full_path.exists()


def get_trend_values(configs: List[SimpleConfig]) -> Dict:
    trend_values = {}
    print(configs)

    for hw in configs:
        if hw.trend:
            for key, item in hw.trend.items():
                try:
                    json_response = requests.get(hw.url, timeout=0.5).json()
                    for nestedKey in item.split('.'):
                        json_response = json_response[nestedKey]
                    trend_values[key] = json_response
                except Exception as e:
                    trend_values[key] = ""

    return trend_values


def get_title(trend_values: Dict) -> str:
    return "timestamp," + ",".join(list(trend_values.keys())) + "\n"


def write_title(title: str, file: Path):
    with open(file, 'w') as f:
        f.write(title)


def create_file_if_missing(today, file_stem, suffix, title):
    if is_trend_file_missing(today, file_stem, suffix):
        file_path = get_path(today, file_stem, suffix + 1)
        file_path.touch(exist_ok=True)
        write_title(title, file_path)


def create_new_file_if_titles_dont_match(today, file_stem, suffix, title):
    file_path = get_path(today, file_stem, suffix)
    with open(file_path, 'r') as f:
        existing_title = f.readline()

    if title != existing_title:
        suffix += 1
        file_path = get_path(today, file_stem, suffix)
        file_path.touch(exist_ok=True)
        write_title(title, file_path)


def write_values(today: str, file_stem, suffix: int, trend_values: Dict):
    file_path = get_path(today, file_stem, suffix)
    values = [str(value) for value in trend_values.values()]
    with open(file_path, 'a') as f:
        line = str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")) + "," + ",".join(values) + "\n"
        f.write(line)


def round_date_to_seconds(date) -> datetime:
    return datetime(date.strftime("%Y-%m-%d %H:%M:%S"))


def round_date_to_days(date) -> datetime:
    return datetime(date.strftime("%Y-%m-%d"))


class Trend(Thread):
    _lock: Lock

    def __init__(self, file_stem: str, to_trend: List[SimpleConfig]):
        Thread.__init__(self)
        self._lock = Lock()
        self.data = None
        self._to_trend = to_trend
        self._file_stem = file_stem

    def get_file_stem(self):
        return self._file_stem

    def run(self):
        Path.mkdir(BASE_PATH, parents=True, exist_ok=True)

        while True:
            time.sleep(1)
            trend_values = get_trend_values(self._to_trend)
            if trend_values == {}:
                continue
            title = get_title(trend_values)

            today = datetime.now().strftime("%Y-%m-%d")
            suffix = get_existing_suffix(today, self._file_stem)
            create_file_if_missing(today, self._file_stem, suffix, title)
            suffix = get_existing_suffix(today, self._file_stem)
            create_new_file_if_titles_dont_match(today, self._file_stem, suffix, title)
            suffix = get_existing_suffix(today, self._file_stem)
            with self._lock:
                write_values(today, self._file_stem, suffix, trend_values)

    def get_last_10_minutes(self):
        right_now = datetime.now()
        before = right_now - timedelta(minutes=10)
        return self.get_values(before, right_now, timedelta(seconds=1))

    def get_last_hour(self):
        right_now = datetime.now()
        before = right_now - timedelta(hours=1)
        return self.get_values(before, right_now, timedelta(seconds=1))

    def get_last_day(self):
        right_now = datetime.now()
        before = right_now - timedelta(days=1)
        return self.get_values(before, right_now, timedelta(seconds=5))

    def get_values(self, start: datetime, end: datetime, step: timedelta):
        frequency = str(step.total_seconds()) + "S"
        start = start.replace(microsecond=0)
        end = end.replace(microsecond=0)
        idx = pd.date_range(start, end, freq=frequency)
        days_in_range = pd.date_range(start.replace(hour=0, minute=0, second=0, microsecond=0),
                                      end.replace(hour=0, minute=0, second=0, microsecond=0), freq='1D')

        valid_days = []
        for d in days_in_range:
            day = d.strftime("%Y-%m-%d")
            suffix = get_existing_suffix(day, self._file_stem)
            valid_days.extend([get_path(day, self._file_stem, x) for x in range(suffix + 1)])

        if not valid_days:
            return ""

        with self._lock:
            dataframes = [pd.read_csv(day) for day in valid_days]
        data = pd.concat(dataframes)
        data['timestamp'] = pd.to_datetime(data['timestamp'])
        data.replace({np.nan: None}, inplace=True)
        data = data.loc[data['timestamp'].isin(idx)]
        values = data.to_dict(orient='list')
        return values
