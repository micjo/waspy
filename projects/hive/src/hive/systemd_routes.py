import logging
import subprocess

from fastapi import HTTPException
from fastapi.responses import FileResponse
from starlette import status
from urllib.parse import urlparse

from hive.config import HiveConfig
from hive.entities import SimpleConfig

def build_systemd_endpoints(router, hive_config: HiveConfig):
    @router.post("/api/service")
    async def service(name: str, start: bool):
        daemon = get_daemon(hive_config, name)
        if not daemon:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail=f'Daemon is not supported')

        start_or_stop = "start" if start else "stop"

        if is_local_daemon(daemon):
            command = f'sudo /bin/systemctl {start_or_stop} {name}'
        else:
            hostname = urlparse(daemon.url).hostname
            command = f'/usr/bin/ssh {hostname}; sudo /bin/systemctl {start_or_stop} {name}'

        logging.info(f"Executing : {command} ")
        subprocess.run([command], shell=True)

    @router.get("/api/service_log/")
    async def service_log(name: str):
        daemon = get_daemon(hive_config, name)
        if not daemon:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail=f'Daemon is not supported')

        if is_local_daemon(daemon):
            command = f'sudo /bin/journalctl -u {name} -n 100 --no-pager'
        else:
            hostname = urlparse(daemon.url).hostname
            command = f'/usr/bin/ssh {hostname}; sudo /bin/journalctl -u {name} -n 100 --no-pager'

        logging.info(f"Executing : {command}")
        output = subprocess.run([command], shell=True, capture_output=True).stdout
        return output

    @router.get("/api/rbs/logs")
    async def get_rbs_logs():
        completed = subprocess.run(["/bin/journalctl --since='1 day ago' | grep -v nginx > /tmp/logs.txt"], shell=True)
        return FileResponse("/tmp/logs.txt")


def is_local_daemon(daemon: SimpleConfig):
    return "127.0.0.1" in daemon.url or "localhost" in daemon.url


def get_daemon(hive_config, name: str) -> SimpleConfig | None:
    if hive_config.erd:
        if hasattr(hive_config.erd.hardware, name):
            return getattr(hive_config.erd.hardware, name)
    if hive_config.rbs:
        if hasattr(hive_config.rbs.hardware, name):
            return getattr(hive_config.rbs.hardware, name)
    if hive_config.any:
        if name in hive_config.any.hardware:
            return hive_config.any.hardware[name]
    return None

