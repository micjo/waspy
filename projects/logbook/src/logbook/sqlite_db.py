import sqlite3
import logging
from pathlib import Path
from typing import List, Union, Annotated
from datetime import datetime
import pandas as pd
import numpy as np
from pydantic import Field

from logbook.entities import ErdRecipeModel, RbsStepwiseRecipe, RbsSingleStepRecipe, RbsStepwiseLeastRecipe, \
    RbsRecipeType, RbsRecipeModel
import time

logging.basicConfig(
    format='[%(asctime)s.%(msecs)03d] [%(levelname)s] %(message)s',
    level=logging.INFO,
    datefmt='%Y.%m.%d__%H:%M__%S')


def build_query(sql_filter=""):
    return f"""
    SELECT l.log_id                                       as log_id,
    l.epoch                                                as epoch,
    l.mode                                                 as mode,
    l.note                                                 as note,
    job_name.name                                          as job_name,
    r.name                                                 as recipe_name,
    r.sample                                               as sample,
    r.start_epoch                                          as start_epoch,
    r.end_epoch                                            as end_epoch,
    r.type                                                 as type,
    r.recipe_id                                            as recipe_id,

    case
    when type is "erd" then
    (select "Z: [" || erd.z_start || "," || erd.z_end || "," || erd.z_increment || "] *" || erd.z_repeat)
    when type is "rbs_random" then
    (select rsteps.axis || ": [" || rsteps.start || "," || rsteps.end || "," || rsteps.step|| "]")
    when type is "rbs_angular_yield" then
    (select rleast.axis || ": [" || rleast.start || "," || rleast.end || "," || rleast.step || "]-> " || rleast.least_yield_position )
    end                                                as move,
    l.meta                                                 as meta
    FROM log_book l
    LEFT join recipe_book r ON l.log_id = r.log_id
    LEFT join job_book j ON l.log_id = j.log_id
    LEFT JOIN job_name_book job_name ON j.job_id = job_name.job_id
    LEFT JOIN rbs_random_book rsteps ON r.recipe_id = rsteps.recipe_id
    LEFT JOIN rbs_angular_yield_book rleast ON r.recipe_id = rleast.recipe_id
    LEFT JOIN erd_book erd ON r.recipe_id = erd.recipe_id
    {sql_filter}
    """


class SqliteDb:
    _sqlite_file: Path
    _active_log_book_row_id: int
    _active_job_id: int

    def __init__(self, sqlite_file: Path):
        self._sqlite_file = sqlite_file
        self._active_log_book_row_id = 0
        self._active_job_id = 0

    def log_job_start(self, name):
        active_log_id = self._add_to_logbook('job', '{} started'.format(name), None)
        self._active_job_id = self.sql_insert("INSERT INTO job_name_book (name)"
                                              " VALUES ('{name}')"
                                              .format(name=name)
                                              )
        self.sql_insert("INSERT INTO job_book (log_id, job_id)"
                        " VALUES ('{log_id}','{job_id}')"
                        .format(log_id=active_log_id, job_id=self._active_job_id)
                        )

    def log_job_finish(self, name: str):
        active_log_id = self._add_to_logbook('job', '{} finished'.format(name), None)
        self.sql_insert("INSERT INTO job_book (log_id, job_id)"
                        " VALUES ('{log_id}','{job_id}')"
                        .format(log_id=active_log_id, job_id=self._active_job_id)
                        )

    def log_job_terminated(self, name: str, reason: str):
        active_log_id = self._add_to_logbook('job', '{name} terminated: {reason}'.format(name=name, reason=reason), None)
        self.sql_insert("INSERT INTO job_book (log_id, job_id)"
                        " VALUES ('{log_id}','{job_id}')"
                        .format(log_id=active_log_id, job_id=self._active_job_id)
                        )

    def log_recipe_finished(self, recipe: RbsRecipeModel | ErdRecipeModel):
        active_log_id = self._add_to_logbook('recipe', '{recipe} finished'.format(recipe=recipe.name), None)
        active_recipe_id = self._add_to_recipe_book(active_log_id, recipe)
        self._log_some_recipe_end(recipe, active_recipe_id)

    def log_recipe_terminated(self, recipe: RbsStepwiseRecipe | RbsSingleStepRecipe |
                                             RbsStepwiseLeastRecipe | ErdRecipeModel, reason: str):
        active_log_id = self._add_to_logbook('recipe', '{recipe} failed: {reason}'.format(recipe=recipe.name, reason=reason), None)
        active_recipe_id = self._add_to_recipe_book(active_log_id, recipe)
        self._log_some_recipe_end(recipe, active_recipe_id)

    def _add_to_logbook(self, mode, message, timestamp: Union[datetime, None]) -> int:
        if timestamp:
            return self.sql_insert("""
                INSERT INTO log_book (mode, note, epoch) VALUES ('{type}', '{message}', '{epoch}');
            """.format(type=mode, message=message, epoch=int(timestamp.timestamp())))
        else:
            return self.sql_insert("""
                INSERT INTO log_book (mode, note) VALUES ('{type}', '{message}');
            """.format(type=mode, message=message))

    def remove_message(self, log_id):
        self.sql_insert("""
            DELETE FROM log_book where log_id='{log_id}'
        """.format(log_id=log_id))

    def log_trend(self, trends: dict):
        columns = ",".join([str(key) for key, value in trends.items() if str(value) != ""])
        surround_values = ",".join([str(value) for value in trends.values() if str(value) != ""])
        self.sql_insert(
            "INSERT INTO trend ({columns}) VALUES ({values});".format(columns=columns, values=surround_values))

    def get_trending(self) -> List[str]:
        response = self._sql_extract("SELECT name FROM pragma_table_info('trend');")
        column_list = response["name"].tolist()
        return column_list

    def get_angle_yields(self, recipe_id) -> List[str]:
        dataframe = self._sql_extract("""
        select angle, yield from rbs_yield_book where recipe_id='{recipe_id}'
        """.format(recipe_id=recipe_id))
        return dataframe.to_dict(orient='records')

    def get_log_messages(self) -> List[str]:
        dataframe = self._sql_extract(build_query())

        dataframe['recipe_id'] = dataframe['recipe_id'].fillna(0).astype(int)
        dataframe.sort_values("epoch", inplace=True)
        dataframe = dataframe.fillna('')
        return dataframe.to_dict(orient='records')

    def get_trend(self, start: datetime, end: datetime, id: str, step: int):
        epoch_start = int(start.timestamp())
        epoch_end = int(end.timestamp())

        dataframe = self._sql_extract("""
           select epoch, {id} from trend where epoch between '{start}' and '{end}'
        """.format(id=id, start=epoch_start, end=epoch_end))
        dataframe.replace({np.nan: None}, inplace=True)
        return dataframe.to_dict(orient='list')

    def get_trend_starts_with(self, start: datetime, end: datetime, starts_with: str, step: int):
        epoch_start = int(start.timestamp())
        epoch_end = int(end.timestamp())
        filtered_columns = [column for column in self.get_trending() if column.startswith(starts_with)]
        filtered_columns_text = ','.join(filtered_columns)
        dataframe = self._sql_extract("""
           select epoch, {column_list} from trend where epoch between '{start}' and '{end}'
        """.format(column_list=filtered_columns_text, start=epoch_start, end=epoch_end, step=step))
        dataframe.replace({np.nan: None}, inplace=True)
        return dataframe.to_dict(orient='list')

    def _sql_extract(self, query) -> pd.DataFrame:
        con = sqlite3.connect(self._sqlite_file)
        df = pd.read_sql_query(query, con)
        con.close()
        return df

    def sql_insert(self, query) -> int:
        logging.debug("executing sql query: {" + query + "}")
        con = sqlite3.connect(self._sqlite_file)
        cur = con.cursor()
        answer = cur.execute(query)
        con.commit()
        con.close()
        return answer.lastrowid

    def _add_to_recipe_book(self, active_log_id, recipe):
        return self.sql_insert("INSERT INTO recipe_book (log_id, job_id, name, sample, type, start_epoch, end_epoch)"
                               " VALUES ('{id}', '{job_id}','{name}','{sample}','{type}','{start_epoch}','{end_epoch}') "
                               .format(id=active_log_id, job_id=self._active_job_id, name=recipe.name,
                                       sample=recipe.sample, type=recipe.type,
                                       start_epoch=int(recipe.start_time.timestamp()),
                                       end_epoch=int(recipe.end_time.timestamp()))
                               )

    def _log_some_recipe_end(self, recipe: RbsStepwiseRecipe | RbsSingleStepRecipe |
                                           RbsStepwiseLeastRecipe | ErdRecipeModel, recipe_id:int):

        if recipe.type == RbsRecipeType.RANDOM:
            self.sql_insert("INSERT INTO rbs_random_book (recipe_id, axis, start, end, step)"
                            "VALUES ('{recipe_id}','{axis}','{start}','{end}','{step}')"
                            .format(recipe_id=recipe_id, axis=recipe.vary_axis, start=recipe.start,
                                    end=recipe.end,
                                    step=recipe.step)
                            )

        if recipe.type == RbsRecipeType.ANGULAR_YIELD:
            self.sql_insert(
                "INSERT INTO rbs_angular_yield_book (recipe_id, axis, start, end, step, least_yield_position)"
                "VALUES ('{recipe_id}','{axis}','{start}','{end}','{step}','{least_yield_position}')"
                    .format(recipe_id=recipe_id, axis=recipe.vary_axis, start=recipe.start,
                            end=recipe.end,
                            step=recipe.step, least_yield_position=recipe.least_yield_position)
            )
            for angleYield in recipe.yield_positions:
                self.sql_insert("INSERT INTO rbs_yield_book (recipe_id, angle, yield)"
                                "VALUES('{recipe_id}','{angle}', '{energy_yield}')"
                                .format(recipe_id=recipe_id, angle=angleYield[0],
                                        energy_yield=angleYield[1]))

        if recipe.type == "erd":
            self.sql_insert("""
                INSERT INTO erd_book (
                recipe_id, theta, z_start, z_end, z_increment, 
                z_repeat, average_terminal_voltage
                )
                VALUES (
                '{id}','{theta}', '{z_start}',
                '{z_end}','{z_increment}','{z_repeat}', '{average_terminal_voltage}'
                );
            """.format(id=recipe_id,
                       sample_id=recipe.sample,
                       theta=recipe.theta,
                       z_start=recipe.z_start,
                       z_end=recipe.z_end,
                       z_increment=recipe.z_increment,
                       z_repeat=recipe.z_repeat,
                       average_terminal_voltage=recipe.average_terminal_voltage))

    def get_filtered_log_messages(self, mode:str, start_time:datetime, end_time:datetime):
        mode_filter = "where"
        if mode == "job":
            mode_filter += ' mode = "job" and'
        elif mode == "recipe":
            mode_filter += ' mode = "recipe" and'

        epoch_start = int(start_time.timestamp())
        epoch_end = int(end_time.timestamp())
        sql_filter = f"{mode_filter} epoch between {epoch_start} and {epoch_end}"
        dataframe = self._sql_extract(build_query(sql_filter))
        dataframe.replace({np.nan: None}, inplace=True)
        return dataframe.to_dict(orient='records')


def datetime_from_utc_to_local(utc_datetime):
    now_timestamp = time.time()
    offset = datetime.fromtimestamp(now_timestamp) - datetime.utcfromtimestamp(now_timestamp)
    return utc_datetime + offset


def datetime_from_local_to_utc(local_datetime):
    now_timestamp = time.time()
    offset = datetime.fromtimestamp(now_timestamp) - datetime.utcfromtimestamp(now_timestamp)
    return local_datetime - offset
