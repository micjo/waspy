from datetime import datetime
from typing import Union

from fastapi import FastAPI
from logbook.sqlite_db import SqliteDb
from logbook.entities import ErdRecipeModel



def add_logbook_routes(router: FastAPI, sql_db: SqliteDb):
    @router.post("/log_message")
    async def log_message(message: str, mode: str = 'note', timestamp: Union[datetime, None] = None):
        sql_db.log_message(mode, message, timestamp)

    @router.post("/remove_message")
    async def remove_message(log_id: int):
        sql_db.remove_message(log_id)

    @router.post("/log_started_job")
    async def log_started_job(job_id: str):
        sql_db.log_message('job', '{job_id} started'.format(job_id=job_id), None)
        return sql_db.get_last_rowid()

    @router.post("/log_finished_job")
    async def log_finished_job(job_id: str):
        sql_db.log_message('job', '{job_id} finished'.format(job_id=job_id), None)

    @router.post("/log_terminated_job")
    async def log_terminated_job(job_id: str, message: str):
        sql_db.log_message('job', '{job_id} terminated: {message}'.format(job_id=job_id, message=message), None)

    @router.post("/log_recipe_finish")
    async def log_recipe_finish(job_type: str, job_id: str, recipe_id: str):
        if job_type == "rbs":
            sql_db.log_rbs_recipe(job_id, recipe_id)

    @router.post("/log_erd_recipe_finish")
    async def log_erd_recipe_finish(erd_recipe_model: ErdRecipeModel):
        sql_db.log_erd_recipe(erd_recipe_model)

    @router.post("/log_trend")
    async def log_trend(trend: dict):
        sql_db.log_trend(trend)

    @router.get("/check_trending")
    async def check_trending():
        return sql_db.get_trending()

    @router.get("/get_log_book")
    async def get_log_book():
        return sql_db.get_log_messages()

    @router.get("/get_rbs_service_log")
    async def get_rbs_service_log():
        return sql_db.get_rbs_service_log()

    @router.get("/get_erd_service_log")
    async def get_erd_service_log(job_id: str):
        return sql_db.get_erd_service_log(job_id)

    @router.get("/get_trend")
    async def get_trend(start: datetime, end: datetime, id: str, step: int):
        return sql_db.get_trend(start, end, id, step)

    @router.get("/get_trend_starts_with")
    async def get_trend_starts_with(start: datetime, end: datetime, starts_with: str, step: int):
        return sql_db.get_trend_starts_with(start, end, starts_with, step)
