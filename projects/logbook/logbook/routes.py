from datetime import datetime

from fastapi import FastAPI
from sqlite_db import SqliteDb
from entities import ErdRecipeModel


def add_logbook_routes(router: FastAPI, sql_db: SqliteDb):
    @router.post("/log_message")
    async def log_message(message: str):
        sql_db.log_message('message', message)

    @router.post("/log_job_start")
    async def log_job_start(job_type: str, job_id: str):
        sql_db.log_message('{job_type}_job'.format(job_type=job_type), '{job_id} started'.format(job_id=job_id))
        return sql_db.get_last_rowid()

    @router.post("/log_job_end")
    async def log_rbs_end(job_type: str, job_id: str):
        sql_db.log_message('{job_type}_job'.format(job_type=job_type), '{job_id} finished'.format(job_id=job_id))

    @router.post("/log_recipe_finish")
    async def log_recipe_finish(row_id: str, job_type: str, job_id: str, recipe_id: str):
        if job_type == "rbs":
            sql_db.log_rbs_recipe(row_id, job_id, recipe_id)

    @router.post("/log_erd_recipe_finish")
    async def log_erd_recipe_finish(row_id:str, erd_recipe_model: ErdRecipeModel):
        sql_db.log_erd_recipe(row_id, erd_recipe_model)

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
    async def get_erd_service_log(row_id: int):
        return sql_db.get_erd_service_log(row_id)

    @router.get("/get_trend")
    async def get_trend(start: datetime, end: datetime, id: str, step: int):
        return sql_db.get_trend(start, end, id, step)

    @router.get("/get_trend_starts_with")
    async def get_trend_starts_with(start: str, end: str, starts_with: str, step: int):
        return sql_db.get_trend_starts_with(start, end, starts_with, step)
