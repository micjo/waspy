# Waspy


# Short description
This repository contains python code to automate, orchestrate and log ion beam analysis.

# How to cite:
- J. Meersschaut and W. Vandervorst, High-throughput ion beam analysis at imec. Nucl. Instrum. Methods Phys. Res., B. 406, 25-29 (2017).
- Michiel Jordens and Johan Meersschaut, WASPy: a Python library to conduct ion beam analysis experiments. [TO BE ADDED] (2022), 

# Repository structure
This is a mono-repo with several projects and libraries. The folder structure is as follows:

  - lib: Contains namespace libraries to be used by projects
  - projects: Contains projects that can be run independently
    - hive: hardware controller automation and orchestration
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

## Python setup
Prerequisites: 
  - Python 3.9.x
  - tox (can be installed through pip or standalone

While python is considered cross-platform, most usage and testing has been done on Linux. Windows should work, this is
however dependent on external libraries, YMMV.

It is good practise to use a virtual environment. Run tox to set up your virtual environment, install the required 
packages and run the unit tests. This may take some time the first time you run it. When running it again, it should be
faster.

```bash
tox
```

After running tox, a folder `venv` will be created. This will contain your virtual environment. 

## Hive
Go to the folder `projects/hive`. To run hive, execute the script `run_hive_local.sh` This will, by default, load the
`default.toml` file, and open a web-server on port 8000. You can change this in the `run_hive_local.sh` script. To 
verify that it is working, open a web-browser and navigate to: `http://localhost:8000`.

(Work in progress)










# Caveats
When using ip addressing, using ''localhost'' can cause unintended slowdowns, particularly in windows. In some cases,
localhost will be treated as an ipv6 address, causing timeouts. Consider using ''127.0.0.1'' instead.


Make sure you have python (3.9.x or higher) and tox installed. Tox wil generate the virtualenv for you and run the tests

Run tox in the repository directory
```
tox
```

You may want to remove the `--reload` option when running in production. It is a useful feature when developing, but it requires extra CPU (about 30% on an i3-9100). If you
do not strictly need it, disable it.


