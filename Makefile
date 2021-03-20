
clean:
	@ ./scripts/manage.sh cleanup

test: clean 
	@ /usr/local/bin/dev/run-pytest.sh

compile: test
	@ ./scripts/manage.sh compile
