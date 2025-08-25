setup:
	python3 -m venv .venv
	.venv/bin/pip install -r requirements.txt
all:
	make build && make install

.PHONY: build
build:
	.venv/bin/pyinstaller main.py --onefile --name gcal

install:
	cp dist/gcal /usr/local/bin

