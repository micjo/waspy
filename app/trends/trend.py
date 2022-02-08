import copy
import json
from threading import Thread
from typing import Dict

from pydantic import BaseModel

from app.hardware_controllers.entities import SimpleConfig
from app.http_routes.http_helper import get_text, get_json, get_json_safe
from pathlib import Path
import time, requests
from datetime import datetime, timedelta
import pandas as pd
import numpy as np
from threading import Lock
from app.setup.config import HiveConfig
from app.rbs.entities import RbsHardware
from app.erd.entities import ErdHardware

BASE_PATH = Path("/root/trends")

def get_path(leader: int, today: str) -> Path:
    return BASE_PATH / "trends_{today}_{leader:03d}.txt".format(today=today, leader=leader)


def get_existing_leader(today: str) -> int:
    i = 0
    while get_path(i, today).exists():
        i += 1
    return i - 1


def is_trend_file_missing(leader: int, today: str) -> bool:
    full_path = get_path(leader, today)
    return not full_path.exists()


class TrendValues(BaseModel):
    aml_x_y: Dict
    motrona: Dict
    zaxis: Dict
    rotation: Dict


def get_trend_values(hive_config: HiveConfig) -> Dict:
    trend_values = {}

    for field, value in hive_config.erd.hardware.__dict__.items():
        hw = SimpleConfig.parse_obj(value)
        if hw.trend:
            for key, item in hw.trend.items():
                try:
                    json_response = requests.get(hw.url, timeout=0.5).json()
                    for nestedKey in item.split('.'):
                        json_response = json_response[nestedKey]
                    trend_values[key] = json_response
                except Exception as e:
                    trend_values[key] = ""

    for field, value in hive_config.rbs.hardware.__dict__.items():
        hw = SimpleConfig.parse_obj(value)
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


def writeTitle(title: str, file: Path):
    with open(file, 'w') as f:
        f.write(title)


def create_file_if_missing(day_leader, today, title):
    if is_trend_file_missing(day_leader, today):
        file_path = get_path(day_leader + 1, today)
        file_path.touch(exist_ok=True)
        writeTitle(title, file_path)


def create_new_file_if_titles_dont_match(day_leader, today, title):
    file_path = get_path(day_leader, today)
    with open(file_path, 'r') as f:
        existing_title = f.readline()

    if title != existing_title:
        day_leader += 1
        file_path = get_path(day_leader, today)
        file_path.touch(exist_ok=True)
        writeTitle(title, file_path)


def write_values(day_leader: int, today: str, trend_values: Dict):
    file_path = get_path(day_leader, today)
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

    def __init__(self, hive_config: HiveConfig):
        Thread.__init__(self)
        self._lock = Lock()
        self.data = None
        self.hive_config = hive_config

    def run(self):
        Path.mkdir(BASE_PATH, parents=True, exist_ok=True)

        while True:
            time.sleep(1)
            trend_values = get_trend_values(self.hive_config)
            title = get_title(trend_values)

            today = datetime.now().strftime("%Y-%m-%d")
            day_leader = get_existing_leader(today)
            create_file_if_missing(day_leader, today, title)
            day_leader = get_existing_leader(today)
            create_new_file_if_titles_dont_match(day_leader, today, title)
            day_leader = get_existing_leader(today)
            write_values(day_leader, today, trend_values)

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
            day_leader = get_existing_leader(day)
            valid_days.extend([get_path(x, day) for x in range(day_leader + 1)])


        dataframes = [pd.read_csv(day) for day in valid_days]
        data = pd.concat(dataframes)
        data['timestamp'] = pd.to_datetime(data['timestamp'])
        data.replace({np.nan: None}, inplace=True)
        data = data.loc[data['timestamp'].isin(idx)]
        values = data.to_dict(orient='list')
        return values
