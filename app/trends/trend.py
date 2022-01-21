import json
from threading import Thread
from app.http_routes.http_helper import get_text, get_json
from pathlib import Path
import time
from datetime import datetime, timedelta
import pandas as pd
from threading import Lock
from app.setup.config import HiveConfig

BASE_PATH = Path("/root/trends")


def get_path(today):
    return BASE_PATH / str("trends_" + today + ".txt")


class Trend(Thread):
    _lock: Lock

    def __init__(self, hive_config: HiveConfig):
        Thread.__init__(self)
        self._lock = Lock()
        self.data = None
        self.hive_config = hive_config

    def run(self):
        Path.mkdir(Path("/tmp/trends/"), parents=True, exist_ok=True)

        while True:
            time.sleep(1)
            current = get_json(self.hive_config.rbs.hardware.motrona.url)["current(nA)"]
            x_position = get_json(self.hive_config.rbs.hardware.aml_x_y.url)["motor_1_position"]
            y_position = get_json(self.hive_config.rbs.hardware.aml_x_y.url)["motor_2_position"]
            ad1_count_rate = get_json(self.hive_config.erd.hardware.mpa3.url)["ad1"]["total_rate"]
            ad2_count_rate = get_json(self.hive_config.erd.hardware.mpa3.url)["ad2"]["total_rate"]
            z_position = get_json(self.hive_config.erd.hardware.mdrive_z.url)["motor_position"]
            rotation_position = get_json(self.hive_config.erd.hardware.mdrive_theta.url)["motor_position"]
            today = datetime.now().strftime("%Y-%m-%d")
            with self._lock:
                if not Path(get_path(today)).is_file():
                    print("file does not exist")
                    with open(get_path(today), 'a') as f:
                        line = "timestamp,ad1_count_rate,ad2_count_rate,z_position,rotation_position,rbs_current,rbs_x,rbs_y\n"
                        f.write(line)

                with open(get_path(today), 'a') as f:
                    line = str(datetime.now().strftime(
                        "%Y-%m-%d %H:%M:%S")) + "," + ad1_count_rate + "," + ad2_count_rate + "," + z_position + "," + rotation_position + "," + current + "," + x_position + "," + y_position + "\n"
                    f.write(line)

                self.data = pd.read_csv(get_path(today))
                self.data['timestamp'] = pd.to_datetime(self.data['timestamp'])

    def get_last_10_minutes(self):
        right_now = datetime.now()
        before = right_now - timedelta(minutes=10)
        idx = pd.date_range(before.strftime("%Y-%m-%d %H:%M:%S"), right_now.strftime("%Y-%m-%d %H:%M:%S"), freq='1S')
        with self._lock:
            return self.data.loc[self.data['timestamp'].isin(idx)].to_dict(orient='list')

    def get_last_hour(self):
        right_now = datetime.now()
        before = right_now - timedelta(hours=1)
        idx = pd.date_range(before.strftime("%Y-%m-%d %H:%M:%S"), right_now.strftime("%Y-%m-%d %H:%M:%S"), freq='1S')
        with self._lock:
            return self.data.loc[self.data['timestamp'].isin(idx)].to_dict(orient='list')

    def get_last_day(self):
        right_now = datetime.now()
        before = right_now - timedelta(days=1)
        idx = pd.date_range(before.strftime("%Y-%m-%d %H:%M:%S"), right_now.strftime("%Y-%m-%d %H:%M:%S"), freq='1S')
        with self._lock:
            return self.data.loc[self.data['timestamp'].isin(idx)].to_dict(orient='list')

    def get_values(self, start: datetime, end: datetime, step: timedelta):
        frequency = str(step.total_seconds()) + "S"
        idx = pd.date_range(start, end, freq=frequency)
        days_in_range = pd.date_range(start.replace(hour=0, minute=0, second=0),
                                      end.replace(hour=0, minute=0, second=0), freq='1D')
        day_files = [d.strftime('/tmp/trends/trends_%Y-%m-%d.txt') for d in days_in_range]

        with self._lock:
            dataframes = [pd.read_csv(day) for day in day_files]
            data = pd.concat(dataframes)
            data['timestamp'] = pd.to_datetime(data['timestamp'])

            return data.loc[data['timestamp'].isin(idx)].to_dict(orient='list')
