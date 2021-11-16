import subprocess

def get_journal():
    completed = subprocess.run(["/bin/journalctl --since='1 hour ago'"], shell=True)
    return completed.stdout

def start_rbs_hardware_controllers():
    # subprocess.run(["sudo /bin/systemctl start aml_x_y aml_det_theta aml_phi_zeta motrona"], shell=True)
    subprocess.run(["sudo /bin/systemctl start smb"], shell=True)

def stop_rbs_hardware_controllers():
    # subprocess.run(["sudo /bin/systemctl stop aml_x_y aml_det_theta aml_phi_zeta motrona"], shell=True)
    subprocess.run(["sudo /bin/systemctl stop smb"], shell=True)
