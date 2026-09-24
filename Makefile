.PHONY: build check list sb clean
build:
	python3 scripts/build.py build
check:
	python3 scripts/build.py check
list:
	python3 scripts/build.py list
sb:
	bash scripts/get-sing-box.sh
clean:
	rm -rf build
