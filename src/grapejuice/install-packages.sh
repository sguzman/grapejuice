#!/usr/bin/env bash

virtualenv -p `which python3` venv
source ./venv/bin/activate
pip install -r requirements.txt

deactivate