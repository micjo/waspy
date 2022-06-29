from pathlib import Path
from waspy.restapi.router_builder import create_router
from logbook.routes import add_logbook_routes
from logbook.sqlite_db import SqliteDb


def main():
    router = create_router(['http://localhost:3000', 'http://localhost:8000'], "/stat")
    sql_db = SqliteDb(Path("hive.db"))

    add_logbook_routes(router, sql_db)
    return router




