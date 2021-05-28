import app.config.home_setup as home_setup
import app.config.lab_setup as lab_setup
from app.config.entities import DaemonConfig, OutputDirConfig, InputDirConfig


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
