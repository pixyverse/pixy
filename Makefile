SHELL := bash
.SHELLFLAGS := -eu -o pipefail -c 
.ONESHELL:
.DELETE_ON_ERROR:
MAKEFLAGS += --warn-undefined-variables
MAKEFLAGS += --no-builtin-rule

VENV = .venv
PYTHON = $(VENV)/bin/python
PIP = $(VENV)/bin/pip
genparser := src/pixyverse/pixy/parser.py
STAMP := .install.stamp



all: venv lint pie test

parser: $(genparser)

venv: $(STAMP)
	source $(VENV)/bin/activate

build: venv
	$(PYTHON) -m build

$(genparser): venv
	$(PYTHON) -m pegen src/pixyverse/pixy/grammar/pypixie.gram -o $(genparser)

$(STAMP): pyproject.toml
	python3 -m venv $(VENV)
	$(PIP) install --upgrade pip	
	. $(VENV)/bin/activate; pip install .[dev]
	touch $(STAMP)

lint: venv 
	# stop the build if there are Python syntax errors or undefined names
	. $(VENV)/bin/activate; flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
	# exit-zero treats all errors as warnings. The GitHub editor is 127 chars wide
	. $(VENV)/bin/activate; flake8 . --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics

pie: $(genparser) $(STAMP)
	# type check with mypy
	. $(VENV)/bin/activate; MYPYPATH=src mypy --namespace-packages --explicit-package-bases .

test: $(genparser) $(STAMP)
	. $(VENV)/bin/activate; python -m unittest

clean:
	rm $(STAMP)
	rm -rf __pycache__
	rm -rf $(VENV)
	rm -rf build
	rm -rf test
	rm -rf $(genparser)

.PHONY: all build clean test lint pie venv