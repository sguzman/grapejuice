#!/usr/bin/env bash

OLD_CWD=`pwd`

PYTHON=`which python3.7`
if [[ ! -f ${PYTHON} ]]; then
    PYTHON=`which python3`
fi

APPLICATION_DIR=$HOME/.local/share/grapejuice
mkdir -p ${APPLICATION_DIR}
cp -frax . ${APPLICATION_DIR}
export PYTHONPATH=${APPLICATION_DIR}/src

cd ${APPLICATION_DIR}
rm -rf ./venv
rm -rf ./.git
rm -rf ./dist
rm -rf ./build

chmod +x ${APPLICATION_DOR}/bin/grapejuice

virtualenv -p ${PYTHON} venv
source ./venv/bin/activate
pip install -r requirements.txt

deactivate

./bin/grapejuice --post_install

cd ${OLD_CWD}
