import logging

import tomli
from starlette.responses import JSONResponse, FileResponse
from fastapi import UploadFile, File

from waspy.iba.file_handler import FileHandler


def add_daybook_routes(router, file_handler: FileHandler, file_name: str):
    @router.post("/daybook")
    async def upload_daybook(file: UploadFile = File(...)):
        logging.info("in upload daybook")
        contents = await file.read()
        content = contents.decode('utf-8')
        logging.info(content)
        try:
            tomli.loads(content)
            return file_handler.write_text_to_disk(file_name, content)
        except tomli.TOMLDecodeError as e:
            return JSONResponse(status_code=400, content=f"Invalid tomli : {e}")

    @router.get("/daybook", response_class=FileResponse)
    async def download_daybook():
        return file_handler.get_local_dir() / file_name

    @router.get("/daybook_json")
    async def download_meta():
        toml = file_handler.read_text_from_disk(file_name)
        return tomli.loads(toml)




