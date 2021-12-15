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
            today = datetime.now().strftime("%Y-%m-%d")
            with self._lock:
                if not Path(get_path(today)).is_file():
                    print("file does not exist")
                    with open(get_path(today), 'a') as f:
                        line = "timestamp,rbs_current,x_position,y_position\n"
                        f.write(line)

                with open(get_path(today), 'a') as f:
                    line = str(datetime.now().strftime(
                        "%Y-%m-%d %H:%M:%S")) + "," + current + "," + x_position + "," + y_position + "\n"
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

    def get_values(self):
        today = datetime.now().strftime("%Y-%m-%d")
        with self._lock:
            data = pd.read_csv(get_path(today))

        data = data.head(10000)
        return data.to_dict(orient='list')
