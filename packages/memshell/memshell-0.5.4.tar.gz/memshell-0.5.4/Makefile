VENV_PATH=./.venv
VENV_BIN=$(VENV_PATH)/bin
RUFF=$(VENV_BIN)/ruff
PYTHON=$(VENV_BIN)/python

format:
	$(RUFF) format --preview .

lint:
	$(RUFF) check .

lint-fix:
	$(RUFF) check --fix .

run:
	$(PYTHON) test.py
