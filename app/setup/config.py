import app.setup.home_setup as home_setup
import app.setup.lab_setup as lab_setup
from app.setup.entities import DaemonConfig, OutputDirConfig, InputDirConfig
import logging
logging.basicConfig(
    format='[%(asctime)s.%(msecs)03d] [%(levelname)s] %(message)s',
    level=logging.INFO,
    datefmt='%Y.%m.%d__%H:%M__%S',
    filename="debug_log.txt")


daemons: DaemonConfig = home_setup.daemons
input_dir: InputDirConfig = home_setup.input_dir
output_dir: OutputDirConfig = home_setup.output_dir
output_dir_remote: OutputDirConfig = home_setup.output_dir_remote

"""
daemons: DaemonConfig = lab_setup.daemons
input_dir: InputDirConfig = lab_setup.input_dir
output_dir: OutputDirConfig = lab_setup.output_dir
output_dir_remote: OutputDirConfig = lab_setup.output_dir_remote
"""
