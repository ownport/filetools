PYTHON ?= /usr/bin/env python3
PROJECT_NAME_BIN ?= filemeta
PROJECT_NAME_SRC ?= src

clean:
	@ echo "[INFO] Cleaning directory:" $(shell pwd)/target
	@ rm -rf $(shell pwd)/target
	@ echo "[INFO] Cleaning files: *.pyc"
	@ find . -name "*.pyc" -delete
	@ echo "[INFO] Cleaning files: .coverage"
	@ rm -rf $(shell pwd)/.coverage

compile: clean
	@ echo "[INFO] Compiling to binary, $(PROJECT_NAME_BIN)"
	@ mkdir -p $(shell pwd)/target
	@ cd $(shell pwd)/src/; zip --quiet -r ../target/$(PROJECT_NAME_BIN) *
	@ echo '#!$(PYTHON)' > target/$(PROJECT_NAME_BIN) && \
		cat target/$(PROJECT_NAME_BIN).zip >> target/$(PROJECT_NAME_BIN) && \
		rm target/$(PROJECT_NAME_BIN).zip && \
		chmod a+x target/$(PROJECT_NAME_BIN)

test: clean
	@ echo "[INFO] Testing ..."
	@ PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=$(shell pwd)/src/ test-suites

test-verbose: clean
	@ echo "[INFO] Testing ..."
	@ PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=$(shell pwd)/src/ test-suites -vv

test-with-coverage: clean
	@ echo "[INFO] Testing ..."
	@ PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=$(shell pwd)/src/ test-suites --cov=${PROJECT_NAME_BIN} \
	    --cov-report term-missing --cov-config=.coveragerc
	@ rm .coverage
