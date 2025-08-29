# Waspy

# Short description
This repository contains python code to automate, orchestrate and log ion beam analysis experiments.

# How to cite:
- J. Meersschaut and W. Vandervorst, High-throughput ion beam analysis at imec. Nucl. Instrum. Methods Phys. Res., B. 406, 25-29 (2017).
- Michiel Jordens and Johan Meersschaut, WASPy: a Python library to conduct ion beam analysis experiments. [TO BE ADDED] (2022), 

# Repository structure
This is a mono-repo with several projects and libraries. The folder structure is as follows:

  - lib: Contains namespace libraries to be used by projects
  - projects: Contains projects that can be run independently
    - mill: hardware controller automation and orchestration
    - logbook: SQL based logging of tasks
    - scripts: Various standalone scripts 
    - trend: Periodically query and log hardware controller parameters
  - service: systemd unit configuration files to run projects as services
  - tests: unit tests

To get more information on the hardware controller support, please reach out to mca\_iba@imec.be. The hardware 
controllers are available as separate software packages through a license model.

# Introduction
To use this code to the fullest, you will require aforementioned hardware controllers. Nonetheless, it can still serve
as an example for using various python packages and libraries. Some packages/libraries used:
  - FastAPI
  - Tox
  - matplotlib
  - pydantic
  - pandas
  - systemd

# Getting Started
To get an overview of what this python code can do for you, have a look at the example files in `projects/scripts/src/scripts/examples`.
These serve as an easy introduction for first time users/readers.

## Python setup
Prerequisites: 
  - Python 3.9.x
  - tox (can be installed through pip or standalone)

While python is considered cross-platform, most usage and testing has been done on Linux. Windows should work, this is
however dependent on external libraries, YMMV.

It is good practise to use a virtual environment. Run tox to set up your virtual environment, install the required 
packages and run the unit tests. This may take some time the first time you run it. When running it again, it should be
faster.

```bash
tox
```

After running tox, a folder `venv` will be created. This will contain your virtual environment. 

## Mill
Go to the folder `projects/mill`. To run mill, execute the script `run_mill_local.sh` This will, by default, load the
`default.toml` file, and open a web-server on port 8000. You can change this in the `run_mill_local.sh` script. To 
verify that it is working, open a web-browser and navigate to: `http://localhost:8000`.

In the `default.toml` configuration file, 2 setups are available. A setup is a logical group of hardware controllers.
The RBS setup consists of:
  - 3 AML stepper motor drivers. (x,y); (phi,zeta); (detector, theta)
  - 1 Motrona DX350 charge counter
  - 1 Caen data acquisition system

The ERD setup consists of:
  - 2 mdrive stepper motor drivers, (z); (theta)
  - 1 mpa3 data acquisition system

Both setups have a folder definition where the experiment (a.k.a 'job') data is stored. This definition is twofold.
The local dir is the main form of storage. All the data here is copied to the remote dir.

For ease of use, a test environment is available as well. This is the 'ANY' setup. It follows the same approach as the
previous setups. You can define and add hardware controllers in a similar fashion. An example is available in the
config file:

e.g :
```toml
[any.hardware.aml_u_v]
type="aml"
title="AML U V"
url="http://localhost:30000/api/latest"
names = ["U", "V"]
```

## Scripts
Go to the folder `projects/scripts`. In here you can find various standalone scripts. You can directly run these. In the
`projects/scripts/examples` directory you can find examples on how to interface with the hardware controllers.

## Logbook
(Work in progress)

## Trend
(work in progress)

# Caveats
- When using ip addressing, using ''localhost'' can cause unintended slowdowns, particularly in windows. In some cases,
localhost will be treated as an ipv6 address, causing timeouts. Consider using ''127.0.0.1'' instead.

- You may want to remove the `--reload` option when running in production. It is a useful feature when developing, but it requires extra CPU (about 30% on an i3-9100). If you
do not strictly need it, disable it.
