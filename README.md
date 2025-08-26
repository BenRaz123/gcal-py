# `gcal`

## Installation

### With venv (recommended)

    make setup
    make build
    sudo make install

Or (does the same thing as above):

    python3 -m venv .venv
    .venv/bin/pip install -r requirements.txt
    .venv/bin/pyinstaller main.py --onefile --name gcal
    sudo cp ./dist/gcal /usr/local/bin # or whatever location you prefer

### No venv (global) (not recommended):

(because you are not using a virtual environment, there is no need for `pyinstaller`)

    pip install -r requirements.txt
    python3 main.py

## Usage

    gcal -h
