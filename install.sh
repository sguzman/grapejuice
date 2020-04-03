#!/usr/bin/env bash

if [ -z ${GRAPEJUICE_INSTALL_PREFIX+x} ]; then
    echo "GRAPEJUICE_INSTALL_PREFIX is not set, quitting..."
    exit 1
fi

if [ ! -d "$GRAPEJUICE_INSTALL_PREFIX" ]; then
    echo "GRAPEJUICE_INSTALL_PREFIX ($GRAPEJUICE_INSTALL_PREFIX) is not a directory, quitting..."
    exit 1
fi

try_deactivate() {
    if command -v deactivate; then
        deactivate
    fi
}

is_command_present() {
    if command -v "$1"; then
        echo "The command $1 is present"
    else
        echo "You are missing the command $1, please follow the Grapejuice installation guide and install all dependencies"
        try_deactivate
        exit 1
    fi
}

virtualenv_failed() {
    echo "Failed to configure virtualenv"
    try_deactivate
    exit 1
}

pip_failed() {
    echo "Failed to install python dependencies"
    try_deactivate
    exit 1
}

python_failed() {
    echo "Failed to call the python interpreter"
    exit 1
}

is_command_present virtualenv

OLD_CWD=$(pwd)

PYTHON=$1
if [[ ! -f "$PYTHON" ]]; then
    python_failed
fi
"$PYTHON" --version || python_failed

APPLICATION_DIR=$GRAPEJUICE_INSTALL_PREFIX/share//grapejuice
mkdir -p "$APPLICATION_DIR"
cp -frax . "$APPLICATION_DIR"
export PYTHONPATH=$APPLICATION_DIR/src

cd "$APPLICATION_DIR" || exit 1
rm -rf ./venv
rm -rf ./.git
rm -rf ./dist
rm -rf ./build

chmod +x "$APPLICATION_DIR/bin/grapejuice"
chmod +x "$APPLICATION_DIR/bin/grapejuiced"

virtualenv -p "$PYTHON" venv || virtualenv_failed
source ./venv/bin/activate
is_command_present pip
pip install -r requirements.txt || pip_failed

deactivate

./bin/grapejuice post_install

case "$GRAPEJUICE_IS_PACKAGING" in
"yes")
    echo "Removing virtualenv since we're packaging"
    rm -rf ./venv
    ;;

esac

cd "$OLD_CWD" || exit 1

echo
echo "Grapejuice is now installed, it should be available in your application launcher or menu."
echo "If Grapejuice does not appear in your menu or launcher, you might have to log out and back in again."
