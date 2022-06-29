import sqlite3
import logging
from pathlib import Path
from typing import List, Union, Annotated
from datetime import datetime
import pandas as pd
import numpy as np
from pydantic import Field

from logbook.entities import ErdRecipeModel, RbsStepwiseRecipe, RbsSingleStepRecipe, RbsStepwiseLeastRecipe, \
    RbsRecipeType
import time

logging.basicConfig(
    format='[%(asctime)s.%(msecs)03d] [%(levelname)s] %(message)s',
    level=logging.INFO,
    datefmt='%Y.%m.%d__%H:%M__%S')


# WARNING: This does no SQL injection checking!

class SqliteDb:
    _sqlite_file: Path
    _active_log_book_row_id: int

    def __init__(self, sqlite_file: Path):
        self._sqlite_file = sqlite_file
        self._active_log_book_row_id = 0

    def log_job_start(self, job):
        self._active_log_book_row_id = self.log_message('job', '{} started'.format(job), None)
        self.sql_insert("INSERT INTO job_book (log_id, job)"
                        " VALUES ('{id}', '{job}')"
                        .format(id=self._active_log_book_row_id, job=job)
                        )

    def log_job_finish(self, job: str):
        self.log_message('job', '{} finished'.format(job), None)

    def log_job_terminated(self, job: str, reason: str):
        self.log_message('job', '{job} terminated: {reason}'.format(job=job, reason=reason), None)

    def log_rbs_recipe(self,
                       rbs_recipe: Annotated[Union[RbsStepwiseRecipe, RbsSingleStepRecipe, RbsStepwiseLeastRecipe],
                                             Field(discriminator='type')]):
        self._active_log_book_row_id = self.log_message('recipe', '{recipe} finished'.format(recipe=rbs_recipe.recipe), None)

        recipe_row_id = self.sql_insert("INSERT INTO recipe_book (log_id, recipe, sample, type, start_epoch, end_epoch)"
                                        " VALUES ('{id}', '{recipe}','{sample}','{type}','{start_epoch}','{end_epoch}') "
                                        .format(id=self._active_log_book_row_id, recipe=rbs_recipe.recipe,
                                                sample=rbs_recipe.sample, type=rbs_recipe.type,
                                                start_epoch=int(rbs_recipe.start_time.timestamp()),
                                                end_epoch=int(rbs_recipe.end_time.timestamp()))
                                        )

        if rbs_recipe.type == RbsRecipeType.STEPWISE:
            self.sql_insert("INSERT INTO rbs_stepwise_book (recipe_id, axis, start, end, step)"
                            "VALUES ('{recipe_id}','{axis}','{start}','{end}','{step}')"
                            .format(recipe_id=recipe_row_id, axis=rbs_recipe.vary_axis, start=rbs_recipe.start,
                                    end=rbs_recipe.end,
                                    step=rbs_recipe.step)
                            )

        if rbs_recipe.type == RbsRecipeType.SINGLE_STEP:
            self.sql_insert("INSERT INTO rbs_single_step_book (recipe_id, axis, position)"
                            "VALUES ('{recipe_id}','{axis}','{position}')"
                            .format(recipe_id=recipe_row_id, axis=rbs_recipe.axis, position=rbs_recipe.position)
                            )

        if rbs_recipe.type == RbsRecipeType.STEPWISE_LEAST:
            self.sql_insert("INSERT INTO rbs_stepwise_least_book (recipe_id, axis, start, end, step, least_yield_position)"
                            "VALUES ('{recipe_id}','{axis}','{start}','{end}','{step}','{least_yield_position}')"
                            .format(recipe_id=recipe_row_id, axis=rbs_recipe.vary_axis, start=rbs_recipe.start,
                                    end=rbs_recipe.end,
                                    step=rbs_recipe.step, least_yield_position=rbs_recipe.least_yield_position)
                            )
            for angleYield in rbs_recipe.yield_positions:
                self.sql_insert("INSERT INTO rbs_yield_book (recipe_id, angle, yield)"
                                "VALUES('{recipe_id}','{angle}', '{energy_yield}')"
                                .format(recipe_id=recipe_row_id, angle=angleYield[0],
                                        energy_yield=angleYield[1]))

    def log_message(self, type, message, timestamp: Union[datetime, None]) -> int:
        if timestamp:
            return self.sql_insert("""
                INSERT INTO log_book (mode, note, epoch) VALUES ('{type}', '{message}', '{epoch}');
            """.format(type=type, message=message, epoch=int(timestamp.timestamp())))
        else:
            return self.sql_insert("""
                INSERT INTO log_book (mode, note) VALUES ('{type}', '{message}');
            """.format(type=type, message=message))

    def remove_message(self, log_id):
        self.sql_insert("""
            DELETE FROM log_book where log_id='{log_id}'
        """.format(log_id=log_id))

    def log_erd_recipe(self, erd_recipe: ErdRecipeModel):
        self.sql_insert("""
            INSERT INTO log_book (mode, epoch) values('erd', '{epoch}')
        """.format(epoch=int(datetime.now().timestamp())))
        self.sql_insert("""
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
        self.sql_insert(
            "INSERT INTO trend ({columns}) VALUES ({values});".format(columns=columns, values=surround_values))

    def get_trending(self) -> List[str]:
        response = self.sql_extract("SELECT name FROM pragma_table_info('trend');")
        column_list = [''.join(item) for item in response]
        return column_list


    def get_angle_yields(self,recipe_id) -> List[str]:
        dataframe = self.sql_extract("""
        select angle, yield from rbs_yield_book where recipe_id='{recipe_id}'
        """.format(recipe_id=recipe_id))
        return dataframe.to_dict(orient='records')

    def get_log_messages(self) -> List[str]:
        dataframe = self.sql_extract("""
        SELECT l.log_id as log_id,
        l.epoch as epoch,
        l.mode as mode,
        l.note as note,
        j.job as job,
        r.recipe as recipe,
        r.sample as sample,
        r.start_epoch as start_epoch,
        r.end_epoch as end_epoch,
        r.type as type,
        r.recipe_id as recipe_id,
        coalesce(rsingle.axis, rsteps.axis,rleast.axis) as axis,
        coalesce(rsingle.position, rsteps.start,rleast.start) as start,
        coalesce(rsteps.step,rleast.step) as step,
        coalesce(rsteps.end,rleast.end) as end,
        l.meta as meta
        FROM log_book l
        LEFT join recipe_book r ON l.log_id=r.log_id
        LEFT join job_book j ON l.log_id= j.log_id
        LEFT JOIN rbs_stepwise_book rsteps ON r.recipe_id = rsteps.recipe_id
        LEFT JOIN rbs_single_step_book rsingle ON r.recipe_id = rsingle.recipe_id
        LEFT JOIN rbs_stepwise_least_book rleast ON r.recipe_id = rleast.recipe_id
        """)

        dataframe['recipe_id'] = dataframe['recipe_id'].fillna(0).astype(int)
        dataframe.sort_values("epoch", inplace=True)
        dataframe = dataframe.fillna('')
        return dataframe.to_dict(orient='records')

    def get_erd_service_log(self, job_id: str):
        columns = ["recipe_name", "sample_id", "beam_type", "beam_energy_MeV", "sample_tilt_degrees", "theta",
                   "z_start", "z_end", "z_increment", "z_repeat", "start_time", "end_time", "average_terminal_voltage",
                   "erd_service_id", "message_id", "erd_name"]
        columns = ','.join(columns)
        dataframe = self.sql_extract("""
           select datetime(utc, 'localtime') as timestamp, {column_list} from erd_service where job_id='{job_id}'
            """.format(column_list=columns, job_id=job_id))
        return dataframe.to_dict(orient='list')

    def get_trend(self, start: datetime, end: datetime, id: str, step: int):
        epoch_start = int(start.timestamp())
        epoch_end = int(end.timestamp())

        dataframe = self.sql_extract("""
           select epoch, {id} from trend where epoch between '{start}' and '{end}'
        """.format(id=id, start=epoch_start, end=epoch_end))
        dataframe.replace({np.nan: None}, inplace=True)
        return dataframe.to_dict(orient='list')

    def get_trend_starts_with(self, start: datetime, end: datetime, starts_with: str, step: int):
        epoch_start = int(start.timestamp())
        epoch_end = int(end.timestamp())
        filtered_columns = [column for column in self.get_trending() if column.startswith(starts_with)]
        filtered_columns_text = ','.join(filtered_columns)
        dataframe = self.sql_extract("""
           select epoch, {column_list} from trend where epoch between '{start}' and '{end}'
        """.format(column_list=filtered_columns_text, start=epoch_start, end=epoch_end, step=step))
        dataframe.replace({np.nan: None}, inplace=True)
        return dataframe.to_dict(orient='list')

    def sql_extract(self, query) -> pd.DataFrame:
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


def datetime_from_utc_to_local(utc_datetime):
    now_timestamp = time.time()
    offset = datetime.fromtimestamp(now_timestamp) - datetime.utcfromtimestamp(now_timestamp)
    return utc_datetime + offset


def datetime_from_local_to_utc(local_datetime):
    now_timestamp = time.time()
    offset = datetime.fromtimestamp(now_timestamp) - datetime.utcfromtimestamp(now_timestamp)
    return local_datetime - offset
