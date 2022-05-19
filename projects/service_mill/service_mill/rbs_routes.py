from hw_control_routes import build_get_redirect, build_post_redirect, build_histogram_redirect, \
    build_packed_histogram
from hive.hardware_control.rbs_setup import RbsSetup


def build_hw_endpoints(http_server, rbs_hardware):
    for key, daemon in rbs_hardware.dict().items():
        build_get_redirect(http_server, daemon['proxy'], daemon['url'], ["RBS"])
        build_post_redirect(http_server, daemon['proxy'], daemon['url'], ["RBS"])
        if daemon['type'] == 'caen':
            build_histogram_redirect(http_server, daemon['proxy'], daemon['url'], ["RBS"])
            build_packed_histogram(http_server, daemon['proxy'], daemon['url'], ["RBS"])


def build_setup_endpoints(http_server, rbs_setup:RbsSetup):
    @http_server.get("/api/rbs/status", tags=["RBS"], summary="Retrieves the rbs status")
    def get_rbs_status():
        return rbs_setup.get_status()

    @http_server.post("/api/rbs/load", tags=["RBS"], summary="Move the rbs setup to the load/unload position")
    def rbs_load(load: bool):
        if load:
            rbs_setup.load()
