#!/usr/bin/env bash

virtualenv3 venv
source ./venv/bin/activate
pip3 install -r requirements.txt

chmod +x grapejuice.py