from pathlib import Path

from db.dashboard_routes import add_dashboard_routes
from db.db_routes import add_logbook_routes
from db.dashboard_handler import DashboardHandler
from waspy.iba.file_handler import FileHandler
from waspy.restapi.router_builder import create_router
from db.sqlite_db import SqliteDb
from pydantic import BaseSettings


class GlobalConfig(BaseSettings):
    DB_FILE: str
    DAYBOOK_FILE: str # TODO: to be removed
    REMOTE_PATH: str
    DASHBOARD_FILE: str # TODO: to be removed
    REMOTE_PATH: str


def main():
    env_conf = GlobalConfig()

    router = create_router(['http://localhost:3000', 'http://localhost:8000'], "/stat")
    sql_db = SqliteDb(Path(env_conf.DB_FILE))
    add_logbook_routes(router, sql_db)

    dashboard_path = Path(env_conf.DASHBOARD_FILE)
    dashboard_folder = dashboard_path.parent
    dashboard_filename = dashboard_path.name

    remote_path = Path(env_conf.REMOTE_PATH)

    remote_path = Path(env_conf.REMOTE_PATH)

    daybook_file_handler = FileHandler(daybook_folder, remote_path)
    dashboard_file_handler = FileHandler(dashboard_folder, remote_path)

    dashboard_handler = DashboardHandler(dashboard_file_handler)

    add_dashboard_routes(router, dashboard_filename, dashboard_handler)

    dashboard_handler.start_update_thread()

    return router