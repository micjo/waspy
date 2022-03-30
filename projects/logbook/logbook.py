from lib.restapi.hive.restapi.router_builder import create_router

def create_app():
    router = create_router(['http://localhost:3000', 'http://localhost'])

    return router




