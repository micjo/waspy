# Waspy

# Short description
This repo contains python code to interface with the hardware controllers. It exposes a number of restapi endpoints.

# Getting started
Make sure you have python (3.9.x or higher) and tox installed. Tox wil generate the virtualenv for you and run the tests

Run tox in the repository directory
```
tox
```

You may want to remove the `--reload` option when running in production. It is a useful feature when developing, but it requires extra CPU (about 30% on an i3-9100). If you
do not strictly need it, disable it.


# How to cite:
  - J. Meersschaut and W. Vandervorst, High-throughput ion beam analysis at imec. Nucl. Instrum. Methods Phys. Res., B. 406, 25-29 (2017).

  - Michiel Jordens and Johan Meersschaut, WASPy: a Python library to conduct ion beam analysis experiments. [TO BE ADDED] (2022), 
