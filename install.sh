#!/usr/bin/env bash

OLD_CWD=`pwd`

APPLICATION_DIR=$HOME/.local/share/grapejuice
mkdir -p ${APPLICATION_DIR}
cp -frax . ${APPLICATION_DIR}
export PYTHONPATH=${APPLICATION_DIR}/src

cd ${APPLICATION_DIR}
virtualenv -p `which python3` venv
source ./venv/bin/activate
pip install -r requirements.txt

deactivate

./bin/grapejuice --post_install

cd ${OLD_CWD}