from fastapi import Body
from starlette.responses import Response, FileResponse

from mill.logbook_db import LogBookDb
from mill.recipe_meta import RecipeMeta
from waspy.iba.erd_setup import ErdSetup
from mill.mill_routes import build_get_redirect, build_post_redirect, build_mpa3_histogram_redirect


def build_driver_endpoints(http_server, erd_hardware):
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


def build_meta_endpoints(http_server, recipe_meta: RecipeMeta):
    @http_server.post("/api/erd/recipe_meta_template", tags=["ERD"], summary="update the experiment metadata template")
    async def upload_erd_recipe_meta_template(meta_template: str = Body(..., media_type="text/plain")):
        return recipe_meta.write_erd_recipe_meta_template(meta_template)

    @http_server.get("/api/erd/recipe_meta_template", tags=["ERD"], summary="get the experiment metadata template", response_class=FileResponse)
    async def download_erd_recipe_meta_template():
        return recipe_meta.get_erd_recipe_meta_template_path()

    @http_server.get("/api/erd/recipe_meta", tags=["ERD"], summary="get the experiment metadata")
    def get_erd_recipe_meta():
        text = recipe_meta.fill_erd_recipe_meta()
        return Response(content=text, media_type="text/plain")
