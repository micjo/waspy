from enum import Enum
from fastapi import APIRouter
import subprocess
import re
from fastapi.responses import FileResponse

from pydantic import BaseModel, validator
router = APIRouter()


class ServiceAction(str, Enum):
    start = 'start'
    stop = 'stop'


class LocalServiceModel(BaseModel):
    action: ServiceAction
    name: str


def only_contain_number_letter_underscore(name: str) -> str:
    if re.match("^[\\w_-]*$", name):
        return name
    raise ValueError('must only contain letters numbers or underscores')


def valid_ip_or_hostname(name: str) -> str:
    if re.match("^[\\w\\.-]*$", name):
        return name
    raise ValueError('must be valid ip address or hostname')


class RemoteServiceModel(BaseModel):
    action: ServiceAction
    name: str
    remote_url: str
    remote_user: str
    _name_check = validator('name', allow_reuse=True)(only_contain_number_letter_underscore)
    _remote_url = validator('remote_url', allow_reuse=True)(valid_ip_or_hostname)
    _remote_user = validator('remote_user', allow_reuse=True)(only_contain_number_letter_underscore)



@router.get("/api/rbs/logs")
async def get_rbs_logs():
    completed = subprocess.run(["/bin/journalctl --since='1 day ago' | grep -v nginx > /tmp/logs.txt"], shell=True)
    return FileResponse("/tmp/logs.txt")


@router.post("/api/rbs/hw_control")
async def hw_control(start: bool):
    # For these commands to work, you have to make sure that these commands can be run without having to provide a
    # password. Look for 'visudo allow command' in a search engine for more information
    if start:
        print("Starting daemons")
        subprocess.run(["/bin/systemctl start aml_x_y aml_det_theta aml_phi_zeta motrona"], shell=True)
        subprocess.run(["/usr/bin/ssh olympus 'sudo systemctl start caen'"], shell=True)
    else:
        print("Stopping daemons")
        subprocess.run(["/bin/systemctl stop aml_x_y aml_det_theta aml_phi_zeta motrona"], shell=True)
        subprocess.run(["/usr/bin/ssh olympus 'sudo systemctl stop caen'"], shell=True)


def build_systemd_endpoints(router):
    @router.post("/api/local_service")

    async def service(service_request: LocalServiceModel):
        command = "/bin/systemctl {action} {name}".format(action=service_request.action, name=service_request.name)
        print(command)

    @router.post("/api/remote_service")
    async def service(service_request: RemoteServiceModel):
        command = "/usr/bin/ssh {user}@{url} '/bin/systemctl {action} {name}'".format(
            user=service_request.remote_user, url=service_request.remote_url, action=service_request.action,
            name=service_request.name)
        print(command)
