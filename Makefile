VENV = .venv
PYTHON = $(VENV)/bin/python
PIP = $(VENV)/bin/pip
genparser := src/pixyverse/pixy/parser.py

all: venv lint pie test

parser: $(genparser)

venv: $(VENV)/bin/activate

build: venv
	$(PYTHON) -m build

$(genparser): venv
	$(PYTHON) -m pegen src/pixyverse/pixy/grammar/pypixie.gram -o $(genparser)

$(VENV)/bin/activate: pyproject.toml
	python3 -m venv $(VENV)
	. $(VENV)/bin/activate
	$(PYTHON) -m pip install --upgrade pip
	$(VENV)/bin/pip install .[dev] 

lint:
	# stop the build if there are Python syntax errors or undefined names
	flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
	# exit-zero treats all errors as warnings. The GitHub editor is 127 chars wide
	flake8 . --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics

pie: $(genparser)
	# type check with mypy
	MYPYPATH=src mypy --namespace-packages --explicit-package-bases .

test: $(genparser)
	cd src && python -m unittest

clean:
	rm -rf __pycache__
	rm -rf $(VENV)
	rm -rf build
	rm -rf test
	rm -rf $(genparser)

.PHONY: all build clean test lint pie