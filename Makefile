
clean:
	@ echo "[INFO] Cleaning directory:" $(shell pwd)/target
	@ rm -rf $(shell pwd)/target
	@ echo "[INFO] Cleaning files: *.pyc"
	@ find . -name "*.pyc" -delete
	@ echo "[INFO] Cleaning files: .coverage"
	@ rm -rf $(shell pwd)/.coverage

test: clean 
	@ echo "[INFO] Running tests" && /usr/local/bin/dev/run-pytest.sh

compile: test
	@ echo "[INFO] Compiling filetools" && ./scripts/manage.sh compile
