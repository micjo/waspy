from pathlib import Path

from db.daybook_routes import add_daybook_routes
from db.db_routes import add_logbook_routes
from waspy.iba.file_handler import FileHandler
from waspy.restapi.router_builder import create_router
from db.sqlite_db import SqliteDb
from pydantic import BaseSettings


class GlobalConfig(BaseSettings):
    DB_FILE: str


def main():
    env_conf = GlobalConfig()

    router = create_router(['http://localhost:3000', 'http://localhost:8000'], "/stat")
    sql_db = SqliteDb(Path(env_conf.DB_FILE))
    add_logbook_routes(router, sql_db)

    daybook_file_handler = FileHandler(Path('./daybook'))
    add_daybook_routes(router, daybook_file_handler)

    return router




