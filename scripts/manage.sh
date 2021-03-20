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
    echo "  clean       :"
    echo "  compile     : compile code to zip package"
    echo
}

function compile() {

    echo "[INFO] Compiling code to zip package" && \
    mkdir -p $(pwd)/target
    cd $(pwd)/src/; zip --quiet -r ../target/${PROJECT_NAME_BIN} *
    echo "#!${PYTHON}" > target/${PROJECT_NAME_BIN} && \
        cat target/${PROJECT_NAME_BIN}.zip >> target/${PROJECT_NAME_BIN} && \
        rm target/${PROJECT_NAME_BIN}.zip && \
        chmod +x target/${PROJECT_NAME_BIN}
}

$@
