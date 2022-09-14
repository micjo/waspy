import http
from datetime import datetime
from typing import Union, Annotated

from fastapi import FastAPI
from pydantic import Field

from logbook.db_orm import DbAccelerator, session, fill_in_entry, insert_dict
from logbook.sqlite_db import SqliteDb
from logbook.entities import ErdRecipeModel, RbsStepwiseRecipe, RbsSingleStepRecipe, RbsStepwiseLeastRecipe, AnyRecipe, \
    Accelerator


def add_logbook_routes(router: FastAPI, sql_db: SqliteDb):
    @router.post("/message")
    async def log_message(message: str, timestamp: Union[datetime, None] = None):
        sql_db._add_to_logbook("note", message, timestamp)

    @router.delete("/message")
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

    @router.post("/log_accelerator_paramaters")
    async def log_accelerator_parameters(accelerator: Accelerator):
        entry = fill_in_entry(accelerator)
        insert_dict(entry)

    @router.delete("/accelerator_parameters", status_code=201)
    async def remove_accelerator_parameters(id: int):
        session.query(DbAccelerator).filter(DbAccelerator.id == id).delete()
        session.commit()

    @router.get("/check_accelerator_parameters")
    async def check_accelerator_parameters():
        return DbAccelerator.__table__.columns.keys()

    @router.get("/get_accelerator_parameters")
    async def check_accelerator_parameters():
        return session.query(DbAccelerator).all()

    @router.get("/get_last_accelerator_parameters")
    async def get_last_accelerator_parameters():
        return session.query(DbAccelerator).order_by(DbAccelerator.epoch.desc()).first()

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

    @router.get("/get_filtered_log_book")
    async def get_filtered_log_book(start: datetime, end: datetime, mode: str = ""):
        return sql_db.get_filtered_log_messages(mode, start, end)

    @router.get("/get_trend")
    async def get_trend(start: datetime, end: datetime, id: str, step: int):
        return sql_db.get_trend(start, end, id, step)

    @router.get("/get_trends_last_day")
    async def get_trends_last_day():
        return sql_db.get_trends_last_day()

    @router.get("/get_trend_starts_with")
    async def get_trend_starts_with(start: datetime, end: datetime, starts_with: str, step: int):
        return sql_db.get_trend_starts_with(start, end, starts_with, step)
