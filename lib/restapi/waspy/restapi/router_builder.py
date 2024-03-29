from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.openapi.docs import get_swagger_ui_html, get_swagger_ui_oauth2_redirect_html


def create_router(origins, static_path) -> FastAPI:
    print("created router")
    app = FastAPI(docs_url=None, redoc_url=None, swagger_ui_parameters={"syntaxHighlight": False})
    app = FastAPI(swagger_ui_parameters={"syntaxHighlight": False})
    static_name = static_path[1:]
    app.mount(static_path, StaticFiles(directory=static_name), name=static_name)

    app.add_middleware(CORSMiddleware, allow_origins=origins, allow_credentials=True,
                       allow_methods=['*'], allow_headers=['*'])

    @app.get("/", include_in_schema=False)
    async def custom_swagger_ui_html():
        return get_swagger_ui_html(
            openapi_url="openapi.json",
            title=app.title + " - Swagger UI",
            oauth2_redirect_url=app.swagger_ui_oauth2_redirect_url,
            swagger_js_url=static_name + "/swagger-ui-bundle.js",
            swagger_css_url=static_name + "/swagger-ui.css",
            swagger_ui_parameters={"syntaxHighlight": False}
        )

    @app.get(app.swagger_ui_oauth2_redirect_url, include_in_schema=False)
    async def swagger_ui_redirect():
        return get_swagger_ui_oauth2_redirect_html()

    @app.get("/favicon.ico")
    def favicon():
        return FileResponse(static_name + '/favicon.png')

    return app
