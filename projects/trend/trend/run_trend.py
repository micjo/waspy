import logging, tomli, requests, time
import sys
import traceback
from datetime import datetime
from enum import Enum
from pathlib import Path

from pydantic import BaseSettings


class LogOption(str, Enum):
    logbook = "logbook"
    stdout = "stdout"
    file = "file"


class GlobalConfig(BaseSettings):
    CONFIG_FILE = "../config.toml"
    LOGBOOK_URL = "http://localhost:8001"
    LOG_TO: LogOption = "stdout"
    FILE_PATH: Path = "trends.txt"


def trend(trend_list):
    logging.info("Loaded config: " + env_conf.json())

    trend_values = {}
    for item in trend_list:
        trend_key, status_url, status_key = item
        try:
            json_response = requests.get(status_url, timeout=0.5).json()
            error_message = json_response["error"]

            for nestedKey in status_key.split('.'):
                json_response = json_response[nestedKey]

            if error_message == "Success" or error_message == "No error":
                trend_values[trend_key] = json_response
            else:
                trend_values[trend_key] = ""
        except Exception as e:
            # print(traceback.format_exc())
            trend_values[trend_key] = ""

    return trend_values


def write_or_check_title(trend_list, env_conf):
    column_titles = [columns[0] for columns in trend_list]

    if env_conf.LOG_TO == LogOption.stdout:
        print("timestamp," + ",".join(column_titles))

    if env_conf.LOG_TO == LogOption.file:
        with open(env_conf.FILE_PATH, 'a') as f:
            f.write("timestamp, " + ",".join(column_titles))
            f.write("\n")

    if env_conf.LOG_TO == LogOption.logbook:
        columns = requests.get(env_conf.LOGBOOK_URL+"/check_trending").json()
        if (set(column_titles).issubset(set(columns))):
            print("database has required columns")
        else:
            print("The database does not contain all the required columns")
            return False

    return True


if __name__ == "__main__":
    env_conf = GlobalConfig()
    with open(env_conf.CONFIG_FILE, "rb") as f:
        conf_from_file = tomli.load(f)
        trend_conf = conf_from_file['trend']

    if not write_or_check_title(trend_conf, env_conf):
        sys.exit("Invalid config. Exitting")

    while True:
        trends = trend(trend_conf)
        values = ",".join([str(x) for x in trends.values()])
        timestamp = str(datetime.now())

        if env_conf.LOG_TO == LogOption.stdout:
            print(timestamp + "," + values)

        if env_conf.LOG_TO == LogOption.file:
            with open(env_conf.FILE_PATH,'a') as f:
                f.write(timestamp + "," + values + "\n")

        if env_conf.LOG_TO == LogOption.logbook:
            try:
                requests.post(env_conf.LOGBOOK_URL + "/log_trend", json=trends)
            except Exception as e:
                print("Could not reach the logbook api. Retrying")


        time.sleep(1)

