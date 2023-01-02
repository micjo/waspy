import tomli
from starlette.responses import JSONResponse, FileResponse
from fastapi import UploadFile

from waspy.iba.file_handler import FileHandler


def add_daybook_routes(router, file_handler: FileHandler):
    @router.post("/daybook")
    async def upload_meta(upload_file: UploadFile):
        content = await upload_file.read()
        try:
            tomli.load(upload_file.file)
            return file_handler.write_text_to_disk('daybook.toml', content.decode("utf-8"))
        except tomli.TOMLDecodeError as e:
            return JSONResponse(status_code=400, content=f"Invalid tomli : {e}")

    @router.get("/daybook", response_class=FileResponse)
    async def download_meta():
        return file_handler.get_local_dir() / "daybook.toml"

    @router.get("/daybook_json")
    async def download_meta():
        toml = file_handler.read_text_from_disk("daybook.toml")
        return tomli.loads(toml)




