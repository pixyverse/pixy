VENV = .venv
PYTHON = $(VENV)/bin/python
PIP = $(VENV)/bin/pip

build: $(VENV)/bin/activate
	$(PYTHON) -m build

genparser: $(VENV)/bin/activate
	$(PYTHON) -m pegen src/pixie/grammar/pypixie.gram -o src/pixie/parser.py

$(VENV)/bin/activate: pyproject.toml
	python3 -m venv $(VENV)
	pip install .[dev]
