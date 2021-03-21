#!/bin/bash

set -e

# Common variables
PYTHON="/usr/bin/env python3"
PROJECT_NAME_BIN="filetools"
PROJECT_NAME_SRC="src"


function help() {

    echo "Usage: ./manage.sh <command>"
    echo 
    echo "Commands:"
    echo "  compile     : compile code to zip package"
    echo
}

function cleanup() {

    CURRENT_DIR=$(pwd)
    echo "[INFO] Cleanup ${CURRENT_DIR%%/}/src/ directory before compile" && \
        [ -d "${CURRENT_DIR}/src/filetools/__pycache__" ] && \
            rm -rf ${CURRENT_DIR}/src/filetools/__pycache__
        [ -d "${CURRENT_DIR}/src/filetools/filetools.egg-info" ] && \
            rm -rf ${CURRENT_DIR}/src/filetools/filetools.egg-info

    echo "[INFO] Cleaning directory:" ${CURRENT_DIR}/dist && \
        rm -rf ${CURRENT_DIR}/dist

    echo "[INFO] Cleaning files: *.pyc" && \
        find . -name "*.pyc" -delete
}

function compile() {

    CURRENT_DIR=$(pwd)
    echo "[INFO] Compiling code to zip package, ${CURRENT_DIR}" && \

    mkdir -p $(pwd)/dist && \
        rm -rf ${pwd}/dist/*
    
    cd $(pwd)/src && zip -r ../dist/${PROJECT_NAME_BIN} * && cd -
    
    echo "#!${PYTHON}" > dist/${PROJECT_NAME_BIN} && \
        cat dist/${PROJECT_NAME_BIN}.zip >> dist/${PROJECT_NAME_BIN} && \
        rm dist/${PROJECT_NAME_BIN}.zip && \
        chmod +x dist/${PROJECT_NAME_BIN}
}

$@
