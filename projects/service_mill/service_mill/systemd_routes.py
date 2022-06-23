import logging
import subprocess

from fastapi import HTTPException
from fastapi.responses import FileResponse
from starlette import status

from config import HiveConfig


def build_systemd_endpoints(router, hive_config: HiveConfig):
    @router.post("/api/service")
    async def service(name: str, start: bool):
        if not (name in hive_config.erd.hardware.__dict__ or name in hive_config.rbs.hardware.__dict__
                or name in hive_config.any.hardware.__root__):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail=f'Daemon is not supported')

        start_or_stop = "start" if start else "stop"
        command = "/bin/systemctl {start_stop} {daemon}".format(start_stop=start_or_stop, daemon=name)

        if name == "caen":
            command = "/usr/bin/ssh olympus 'sudo " + command + "'"

        logging.info("Executing : {" + command + "}")
        subprocess.run([command], shell=True)

    @router.get("/api/service_log")
    async def service(daemon: str):
        if not (daemon in hive_config.erd.hardware.__dict__ or daemon in hive_config.rbs.hardware.__dict__
                or daemon in hive_config.any.hardware.__root__):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail=f'Daemon is not supported')
        command = '/bin/journalctl -u {daemon} --since="10 minutes ago"'.format(daemon=daemon)
        logging.info("Executing : {" + command + "}")
        output = subprocess.run([command], shell=True, capture_output=True).stdout
        return output

    @router.get("/api/rbs/logs")
    async def get_rbs_logs():
        completed = subprocess.run(["/bin/journalctl --since='1 day ago' | grep -v nginx > /tmp/logs.txt"], shell=True)
        return FileResponse("/tmp/logs.txt")

    @router.post("/api/rbs/hw_control")
    async def hw_control(start: bool):
        # For these commands to work, you have to make sure that these commands can be run without having to provide a
        # password. Look for 'visudo allow command' in a search engine for more information
        if start:
            logging.info("Starting daemons")
            subprocess.run(["/bin/systemctl start aml_x_y aml_det_theta aml_phi_zeta motrona"], shell=True)
            subprocess.run(["/usr/bin/ssh olympus 'sudo systemctl start caen'"], shell=True)
        else:
            logging.info("Stopping daemons")
            subprocess.run(["/bin/systemctl stop aml_x_y aml_det_theta aml_phi_zeta motrona"], shell=True)
            subprocess.run(["/usr/bin/ssh olympus 'sudo systemctl stop caen'"], shell=True)


