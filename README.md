# Hive

# Short description
This repo contains python code to interface with the hardware controllers. It exposes a number of restapi endpoints.

# Getting started
Make sure you have python (3.9.x or higher) installed. It is recommended to use a virtual environment to run this. You can make use of the setup.py file to install all the dependencies.

Setup a virtual environment in the pyvenv folder. You can choose a folder name:
```
python -m venv pyvenv 
```

Load the virtual environment by sourcing the activate script on linux, or running the activate.bat script in windows. These are located in `pyvenv/bin`
On linux (Unix):
```
source pyvenv/bin/activate
```
on Windows:
```
pyvenv/bin/activate.bat
```

Install the dependencies. Pip will search for a setup.py in the mentioned folder (`dot` is the current folder), and install the required packages
```
pip install .
```

Start the script.
On Linux (Unix):
```
./run.sh
```
On Windows:
```
run.bat
```

You may want to remove the `--reload` option when running in production. It is a useful feature when developing, but it requires extra CPU (about 30% on an i3-9100). If you
do not strictly need it, disable it.

