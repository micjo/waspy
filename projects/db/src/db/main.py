from pathlib import Path
from waspy.restapi.router_builder import create_router
from db.routes import add_logbook_routes
from db.sqlite_db import SqliteDb
from pydantic import BaseSettings


class GlobalConfig(BaseSettings):
    DB_FILE : str


def main():
    env_conf = GlobalConfig()

    router = create_router(['http://localhost:3000', 'http://localhost:8000'], "/stat")
    sql_db = SqliteDb(Path(env_conf.DB_FILE))

    add_logbook_routes(router, sql_db)
    return router




