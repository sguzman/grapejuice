#!/usr/bin/env bash

export LD_LIBRARY_PATH=/usr/local/lib

SCRIPT=$(readlink -f $0)
SCRIPT_DIR=`dirname ${SCRIPT}`

exec ${SCRIPT_DIR}/build.sh