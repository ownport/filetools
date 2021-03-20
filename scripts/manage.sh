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

function compile() {

    CURRENT_DIR=$(pwd)
    echo "[INFO] Compiling code to zip package, ${CURRENT_DIR}" && \

    echo "[INFO] Cleanup ${CURRENT_DIR%%/}/src/ directory before compile" && \
        [ -d "${CURRENT_DIR}/src/filetools/__pycache__" ] && \
            rm -rf ${CURRENT_DIR}/src/filetools/__pycache__
        [ -d "${CURRENT_DIR}/src/filetools/filetools.egg-info" ] && \
            rm -rf ${CURRENT_DIR}/src/filetools/filetools.egg-info

    mkdir -p $(pwd)/target && \
        rm -rf ${pwd}/target/*
    
    cd $(pwd)/src && zip -r ../target/${PROJECT_NAME_BIN} * && cd -
    
    echo "#!${PYTHON}" > target/${PROJECT_NAME_BIN} && \
        cat target/${PROJECT_NAME_BIN}.zip >> target/${PROJECT_NAME_BIN} && \
        rm target/${PROJECT_NAME_BIN}.zip && \
        chmod +x target/${PROJECT_NAME_BIN}
}

$@
