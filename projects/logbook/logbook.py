from hive.restapi.router_builder import create_router
from routes import add_logbook_routes


def main():
    router = create_router(['http://localhost:3000', 'http://localhost:8000'], "/stat")
    add_logbook_routes(router)
    return router




