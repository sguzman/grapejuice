#!/usr/bin/env bash

OLD_CWD=`pwd`

PYTHON=`which python3`
RUNNER_NAME=01_grapejuice

SCRIPT=$(readlink -f $0)
SCRIPT_DIR=`dirname ${SCRIPT}`
PKG_SRC_DIR=${SCRIPT_DIR}/src
PROJECT_DIR=`realpath ${SCRIPT_DIR}/../../`
ASSETS_DIR=${PROJECT_DIR}/assets
VERSION_FILE=${PROJECT_DIR}/src/grapejuice/__init__.py
PY_RUNNER=${PROJECT_DIR}/${RUNNER_NAME}.py
DIST_DIR=${PROJECT_DIR}/dist
APP_DIST_DIR=${DIST_DIR}/${RUNNER_NAME}
VENV=${PROJECT_DIR}/venv
APPIMAGE_DIR=${DIST_DIR}/grapejuice.AppDir
APPIMAGE_TOOL=${DIST_DIR}/AppImageTool.AppImage

export PYTHONPATH=${PROJECT_DIR}/src

cd ${PROJECT_DIR}
rm -rf ${DIST_DIR}

if [[ ! -d ${VENV} ]]; then
    ${PYTHON} -m venv ${VENV}
fi
source ${VENV}/bin/activate
pip install -r ${PROJECT_DIR}/requirements.txt
python bdist_wheel
find dist -iname \*.whl -exec pip install {} \;
pyinstaller ${PY_RUNNER}

deactivate

cp -frax ${ASSETS_DIR} ${APP_DIST_DIR}
cp ${ASSETS_DIR}/grapejuice-128.png ${APP_DIST_DIR}/grapejuice.png
cp ${VERSION_FILE} ${APP_DIST_DIR}
cp -frax ${PKG_SRC_DIR}/* ${APP_DIST_DIR}

rm -rf ${APP_DIST_DIR}/share/icons
rm -rf ${APP_DIST_DIR}/share/themes

APP_LOCALE_DIR=${APP_DIST_DIR}/share/locale
for locale in `ls ${APP_LOCALE_DIR} | grep -v ^en`; do
    rm -rf ${APP_LOCALE_DIR}/${locale}
done

mv ${APP_DIST_DIR} ${APPIMAGE_DIR}

wget 'https://github.com/AppImage/AppImageKit/releases/download/continuous/appimagetool-x86_64.AppImage' -O ${APPIMAGE_TOOL}
chmod +x ${APPIMAGE_TOOL}
cd ${DIST_DIR}
${APPIMAGE_TOOL} ${APPIMAGE_DIR}

cd ${OLD_CWD}
