from waspy.hardware_control.erd_setup import ErdSetup
from hw_control_routes import build_get_redirect, build_post_redirect, build_mpa3_histogram_redirect


def build_hw_endpoints(http_server, erd_hardware):
    for key, daemon in erd_hardware.dict().items():
        build_get_redirect(http_server, daemon['proxy'], daemon['url'], ["ERD"])
        build_post_redirect(http_server, daemon['proxy'], daemon['url'], ["ERD"])
        if daemon['type'] == 'mpa3':
            build_mpa3_histogram_redirect(http_server, daemon['proxy'], daemon['url'], ["ERD"])


def build_setup_endpoints(http_server, erd_setup:ErdSetup):
    @http_server.get("/api/erd/status", tags=["ERD"])
    def get_rbs_status():
        return erd_setup.get_status()

    @http_server.post("/api/erd/load", tags=["ERD"])
    def get_rbs_status(load: bool):
        if load:
            erd_setup.load()
