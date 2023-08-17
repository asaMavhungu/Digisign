# Makefile for Python Project

# Variables
VENV_NAME = .venv
PYTHON = $(VENV_NAME)/bin/python
PIP = $(VENV_NAME)/bin/pip

# Targets and Rules
.PHONY: setup install run test clean

# Set up the virtual environment
setup:
	python3 -m venv $(VENV_NAME)
	$(PIP) install --upgrade pip

# Install project dependencies
install: setup
	$(PIP) install -r requirements.txt

# Run your Python script
run: install
	$(PYTHON) main.py

# Run tests
test: install
	$(PYTHON) -m pytest

# Clean up generated files and virtual environment
clean:
	rm -rf $(VENV_NAME)
	find . -type f -name "*.pyc" -delete
