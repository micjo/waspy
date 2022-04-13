import sqlite3
import logging
from pathlib import Path
from typing import List
import pandas as pd
import numpy as np

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
        self._exec("INSERT INTO log_book (type, message) VALUES ('{type}', '{message}');".format(type=type, message=message))

    def log_rbs_recipe(self, row_id: str, rbs: str, recipe_name: str):
        self._exec("""
            INSERT INTO rbs_service_log (message_id, rbs_name, recipe_name)
            VALUES ('{id}', '{rbs}', '{recipe}');
        """.format(id=row_id, rbs=rbs, recipe=recipe_name))

    def log_erd_recipe(self, row_id: str, erd: str, recipe_name: str):
        self._exec("""
            INSERT INTO erd_service_log (message_id, erd_name, recipe_name)
            VALUES ('{id}', '{erd}', '{recipe}');
        """.format(id=row_id, erd=erd, recipe=recipe_name))

    def log_trend(self, trends: dict):
        columns = ",".join([str(key) for key, value in trends.items() if str(value) != ""])
        surround_values = ",".join([str(value) for value in trends.values() if str(value) != ""])
        self._exec("INSERT INTO trend ({columns}) VALUES ({values});".format(columns=columns, values=surround_values))

    def get_trending(self) -> List[str]:
        response = self._exec("SELECT name FROM pragma_table_info('trend');")
        column_list = [''.join(item) for item in response]
        return column_list

    def get_trend(self, start: str, end: str, id: str, step: int):
        dataframe = self._exec_panda("""
           select datetime(utc, 'localtime') as timestamp, {id} from trend where datetime(utc, 'localtime') between '{start}' and '{end}'
           and strftime("%S", utc) % '{step}' == 0
        """.format(id=id, start=start, end=end, step=step))
        dataframe.replace({np.nan: None}, inplace=True)
        return dataframe.to_dict(orient='list')

    def get_trend_starts_with(self, start: str, end: str, starts_with: str, step: int):
        filtered_columns = [column for column in self.get_trending() if column.startswith(starts_with)]
        filtered_columns_text = ','.join(filtered_columns)
        dataframe = self._exec_panda("""
           select datetime(utc, 'localtime') as timestamp, {column_list} from trend where datetime(utc, 'localtime') between '{start}' and '{end}'
           and strftime("%S", utc) % '{step}' == 0
        """.format(column_list=filtered_columns_text, start=start, end=end, step=step))
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
