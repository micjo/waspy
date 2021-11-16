from fastapi import APIRouter
import subprocess
from fastapi.responses import FileResponse

router = APIRouter()


@router.get("/api/rbs/logs")
async def get_rbs_logs():
    completed = subprocess.run(["/bin/journalctl -q --no-pager --since='1 day ago' > /tmp/logs.txt"], shell=True)
    return FileResponse("/tmp/logs.txt")


@router.post("/api/rbs/hw_control")
async def hw_control(start: bool):
    # For these commands to work, you have to make sure that these commands can be run without having to provide a
    # password. Look for 'visudo allow command' in a search engine for more information
    if start:
        # subprocess.run(["sudo /bin/systemctl start aml_x_y aml_det_theta aml_phi_zeta motrona"], shell=True)
        subprocess.run(["sudo /bin/systemctl start smb"], shell=True)
    else:
        # subprocess.run(["sudo /bin/systemctl stop aml_x_y aml_det_theta aml_phi_zeta motrona"], shell=True)
        subprocess.run(["sudo /bin/systemctl stop smb"], shell=True)

