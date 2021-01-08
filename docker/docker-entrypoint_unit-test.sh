#!/bin/bash
eval "pip install -e ."
eval "pytest --cov-report xml --cov-report term --cov=src/casymda/ tests"
