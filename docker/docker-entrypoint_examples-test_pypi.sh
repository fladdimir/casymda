#!/bin/bash
# lets do a complete package install from pypi and see if the examples work
eval "pip install casymda"
eval "python3 -m pytest examples"
