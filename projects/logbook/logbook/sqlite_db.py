import sqlite3
import logging
from pathlib import Path
from typing import List
from datetime import datetime
import pandas as pd
import numpy as np
from entities import ErdRecipeModel
import time

logging.basicConfig(
    format='[%(asctime)s.%(msecs)03d] [%(levelname)s] %(message)s',
    level=logging.INFO,
    datefmt='%Y.%m.%d__%H:%M__%S')


# WARNING: This does no SQL injection checking!

class SqliteDb:
    _sqlite_file: Path
    _last_rowid: str

    def __init__(self, sqlite_file: Path):
        self._sqlite_file = sqlite_file

    def get_last_rowid(self):
        return self._last_rowid

    def log_message(self, type, message):
        self._exec("""
            INSERT INTO log_book (mode, note, epoch) VALUES ('{type}', '{message}, {epoch}');
        """.format(type=type, message=message, epoch=int(datetime.now().timestamp())))

    def log_rbs_recipe(self, job_id: str, recipe_name: str):
        self._exec("""
            INSERT INTO log_book (mode, epoch) values('rbs', '{epoch}')
        """.format(epoch=int(datetime.now().timestamp())))
        self._exec("""
            INSERT INTO rbs_service (log_id, job_id, recipe_name)
            VALUES ('{id}', '{job_id}', '{recipe}');
        """.format(id=self._last_rowid, job_id=job_id, recipe=recipe_name))

    def log_erd_recipe(self, erd_recipe: ErdRecipeModel):
        self._exec("""
            INSERT INTO log_book (mode, epoch) values('erd', '{epoch}')
        """.format(epoch=int(datetime.now().timestamp())))
        self._exec("""
            INSERT INTO erd_service 
            (log_id, job_id, beam_type, beam_energy_MeV, sample_tilt_degrees, sample_id, 
            recipe_name, theta, z_start, z_end, z_increment, z_repeat, 
            start_time, end_time, average_terminal_voltage)
            VALUES (
            '{id}', '{job_id}', '{beam_type}', '{beam_energy_MeV}', '{sample_tilt_degrees}', '{sample_id}', 
            '{file_stem}', '{theta}', '{z_start}','{z_end}','{z_increment}','{z_repeat}',
            '{start_time}','{end_time}','{avg_terminal_voltage}'
            );
        """.format(id=self._last_rowid,
                   job_id=erd_recipe.job_id,
                   beam_type=erd_recipe.beam_type,
                   beam_energy_MeV=erd_recipe.beam_energy_MeV,
                   sample_tilt_degrees=erd_recipe.sample_tilt_degrees,
                   sample_id=erd_recipe.sample_id,
                   file_stem=erd_recipe.file_stem,
                   theta=erd_recipe.theta,
                   z_start=erd_recipe.z_start,
                   z_end=erd_recipe.z_end,
                   z_increment=erd_recipe.z_increment,
                   z_repeat=erd_recipe.z_repeat,
                   start_time=int(erd_recipe.start_time.timestamp()),
                   end_time=int(erd_recipe.end_time.timestamp()),
                   avg_terminal_voltage=erd_recipe.avg_terminal_voltage))

    def log_trend(self, trends: dict):
        columns = ",".join([str(key) for key, value in trends.items() if str(value) != ""])
        surround_values = ",".join([str(value) for value in trends.values() if str(value) != ""])
        self._exec("INSERT INTO trend ({columns}) VALUES ({values});".format(columns=columns, values=surround_values))

    def get_trending(self) -> List[str]:
        response = self._exec("SELECT name FROM pragma_table_info('trend');")
        column_list = [''.join(item) for item in response]
        return column_list

    def get_log_messages(self) -> List[str]:
        dataframe = self._exec_panda("""
        SELECT l.epoch as epoch,
       l.mode as mode,
       l.note as note,
       coalesce(e.job_id, r.job_id) as job_id,
       coalesce(e.recipe_name, r.recipe_name) as recipe_name,
       coalesce(e.sample_id, r.sample_id) as sample_id,
       coalesce(e.start_time, r.start_time) as start_time,
       coalesce(e.end_time, r.end_time) as end_time,
       l.meta as meta
        FROM log_book l
        LEFT JOIN erd_service e
        ON l.log_id= e.log_id
        LEFT join rbs_service r
        ON l.log_id = r.log_id;
        """)

        dataframe.sort_values("epoch", inplace=True)
        dataframe = dataframe.fillna('')
        return dataframe.to_dict(orient='records')

    def get_erd_service_log_title(self) -> List[str]:
        response = self._exec("SELECT name FROM pragma_table_info('erd_service');")
        column_list = [''.join(item) for item in response]
        return column_list

    def get_rbs_service_log(self) -> List[str]:
        return self._exec("SELECT * FROM rbs_service;")

    def get_erd_service_log(self, job_id: str):
        columns = ["recipe_name", "sample_id", "beam_type", "beam_energy_MeV", "sample_tilt_degrees", "theta",
                   "z_start", "z_end", "z_increment", "z_repeat", "start_time", "end_time", "average_terminal_voltage",
                   "erd_service_id", "message_id", "erd_name"]
        columns = ','.join(columns)
        dataframe = self._exec_panda("""
           select datetime(utc, 'localtime') as timestamp, {column_list} from erd_service where job_id='{job_id}'
            """.format(column_list=columns, job_id=job_id))
        return dataframe.to_dict(orient='list')

    def get_trend(self, start: datetime, end: datetime, id: str, step: int):
        epoch_start = int(start.timestamp())
        epoch_end = int(end.timestamp())

        dataframe = self._exec_panda("""
           select epoch, {id} from trend where epoch between '{start}' and '{end}'
        """.format(id=id, start=epoch_start, end=epoch_end))
        dataframe.replace({np.nan: None}, inplace=True)
        return dataframe.to_dict(orient='list')

    def get_trend_starts_with(self, start: datetime, end: datetime, starts_with: str, step: int):
        epoch_start = int(start.timestamp())
        epoch_end = int(end.timestamp())
        filtered_columns = [column for column in self.get_trending() if column.startswith(starts_with)]
        filtered_columns_text = ','.join(filtered_columns)
        dataframe = self._exec_panda("""
           select epoch, {column_list} from trend where epoch between '{start}' and '{end}'
        """.format(column_list=filtered_columns_text, start=epoch_start, end=epoch_end, step=step))
        dataframe.replace({np.nan: None}, inplace=True)
        return dataframe.to_dict(orient='list')

    def _exec_panda(self, query):
        con = sqlite3.connect(self._sqlite_file)
        df = pd.read_sql_query(query, con)
        con.close()
        return df

    def _exec(self, query):
        logging.debug("executing sql query: {" + query + "}")
        con = sqlite3.connect(self._sqlite_file)
        cur = con.cursor()
        answer = cur.execute(query)
        con.commit()
        response = answer.fetchall()
        con.close()
        self._last_rowid = answer.lastrowid
        return response


def datetime_from_utc_to_local(utc_datetime):
    now_timestamp = time.time()
    offset = datetime.fromtimestamp(now_timestamp) - datetime.utcfromtimestamp(now_timestamp)
    return utc_datetime + offset


def datetime_from_local_to_utc(local_datetime):
    now_timestamp = time.time()
    offset = datetime.fromtimestamp(now_timestamp) - datetime.utcfromtimestamp(now_timestamp)
    return local_datetime - offset
