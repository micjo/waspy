from datetime import datetime
from typing import Union, Annotated

from fastapi import FastAPI
from pydantic import Field

from logbook.sqlite_db import SqliteDb
from logbook.entities import ErdRecipeModel, RbsStepwiseRecipe, RbsSingleStepRecipe, RbsStepwiseLeastRecipe, AnyRecipe


def add_logbook_routes(router: FastAPI, sql_db: SqliteDb):
    @router.post("/log_message")
    async def log_message(message: str, mode: str = 'note', timestamp: Union[datetime, None] = None):
        sql_db.add_to_logbook(mode, message, timestamp)

    @router.post("/remove_message")
    async def remove_message(log_id: int):
        sql_db.remove_message(log_id)

    @router.post("/log_started_job")
    async def log_started_job(name: str):
        return sql_db.log_job_start(name)

    @router.post("/log_finished_job")
    async def log_finished_job(name: str):
        return sql_db.log_job_finish(name)

    @router.post("/log_terminated_job")
    async def log_terminated_job(name: str, reason: str):
        return sql_db.log_job_terminated(name, reason)

    @router.post("/log_finished_recipe")
    async def log_finished_recipe(rbs_recipe: AnyRecipe):
        sql_db.log_recipe_finished(rbs_recipe.__root__)

    @router.post("/log_terminated_recipe")
    async def log_terminated_recipe(rbs_recipe: AnyRecipe, reason: str):
        sql_db.log_recipe_terminated(rbs_recipe.__root__, reason)

    @router.post("/log_trend")
    async def log_trend(trend: dict):
        sql_db.log_trend(trend)

    @router.get("/check_trending")
    async def check_trending():
        return sql_db.get_trending()

    @router.get("/get_log_book")
    async def get_log_book():
        return sql_db.get_log_messages()

    @router.get("/get_trend")
    async def get_trend(start: datetime, end: datetime, id: str, step: int):
        return sql_db.get_trend(start, end, id, step)

    @router.get("/get_trend_starts_with")
    async def get_trend_starts_with(start: datetime, end: datetime, starts_with: str, step: int):
        return sql_db.get_trend_starts_with(start, end, starts_with, step)
