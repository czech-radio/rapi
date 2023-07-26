VENV = ./.venv
PYTHON = $(VENV)/bin/python3
PIP = $(VENV)/bin/pip

install: $(VENV)/bin/activate
	source $(VENV)/bin/activate;
	$(PIP) install --upgrade pip
	$(PIP) install -e .[dev];

$(VENV)/bin/activate:
	python3 -m venv $(VENV)

run:
	$(VENV)/bin/rapi

clean:
	rm -rf ./src/rapi/__pycache__/
	rm -rf ./src/rapi.egg-info/
	rm -rf ./.pytest_cache/
	rm -rf ./.mypy_cache/


