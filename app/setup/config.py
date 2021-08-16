import app.setup.home_setup as home_setup
import app.setup.lab_setup as lab_setup
import app.setup.container_setup as container_setup
from app.setup.entities import DaemonConfig, OutputDirConfig, InputDirConfig
import logging
import tomli
logging.basicConfig(
    format='[%(asctime)s.%(msecs)03d] [%(levelname)s] %(message)s',
    level=logging.INFO,
    datefmt='%Y.%m.%d__%H:%M__%S',
    filename="debug_log.txt")


with open("./config.toml", "rb") as f:
    hw_config = tomli.load(f)


daemons = DaemonConfig.parse_obj(hw_config['hw_control'])
input_dir = InputDirConfig.parse_obj(hw_config['rbs']['input_dir'])
output_dir = OutputDirConfig.parse_obj(hw_config['rbs']['output_dir'])
output_dir_remote = OutputDirConfig.parse_obj(hw_config['rbs']['remote_output_dir'])

"""
daemons: DaemonConfig = lab_setup.daemons
input_dir: InputDirConfig = lab_setup.input_dir
output_dir: OutputDirConfig = lab_setup.output_dir
output_dir_remote: OutputDirConfig = lab_setup.output_dir_remote
"""
