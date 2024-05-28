# Makefile

# Explicitly use Python 3 (replace 'python3' with the path if it's not in your PATH)
PYTHON := python3

# Virtual environment directory
VENV := .venv

# Virtual environment setup
.PHONY: venv
venv: $(VENV)  # This is a phony target since 'venv' is a directory
$(VENV): requirements.txt
	$(PYTHON) -m venv $(VENV)
	$(VENV)/bin/pip install --upgrade pip
	$(VENV)/bin/pip install -r requirements.txt

# Cleaning up
.PHONY: clean
clean:
	rm -rf $(VENV)