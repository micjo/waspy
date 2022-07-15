import traceback
from pathlib import Path

from fastapi import UploadFile, File
from fastapi.responses import FileResponse
from starlette import status
from starlette.responses import Response

from waspy.restapi.router_builder import create_router
import logging
import subprocess

logging.basicConfig(
    format='[%(asctime)s.%(msecs)03d] [%(levelname)s] %(message)s',
    level=logging.INFO,
    datefmt='%Y.%m.%d__%H:%M__%S')


def main():
    router = create_router(['http://localhost:3000', 'http://localhost:8000'], "/stat")

    @router.post("/simulate_spectrum")
    async def simulate_spectrum(response: Response, file: UploadFile = File(...)):
        try:
            file_bytes = await file.read()
            contents = file_bytes.decode('utf-8')
            with open("ruthelde-in.json", "w") as f:
                f.write(contents)

            subprocess.call(['java', '-jar', 'ruthelde.jar', 'simulate', 'ruthelde-in.json', 'testfile.imec'])
            return FileResponse("testfile.imec")

        except Exception as e:
            logging.error(traceback.format_exc())
            response.status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
            return str(e)

    return router




