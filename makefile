# Makefile for Flask project

# Define the main Python file (change this if your main file has a different name)
MAIN_FILE := app.py

# Python interpreter
PYTHON := python3

# Name of the virtual environment directory
VENV_NAME := .venv

# Directories
APP_DIR := project
TESTS_DIR := tests

# Targets and Commands
.PHONY: run
run: venv
	@echo "Running the Flask app..."
	@. $(VENV_NAME)/bin/activate; $(PYTHON) $(APP_DIR)/$(MAIN_FILE)

.PHONY: test
test: venv
	@echo "Running tests..."
	@. $(VENV_NAME)/bin/activate; $(PYTHON) -m pytest $(TESTS_DIR)

venv: $(VENV_NAME)/bin/activate

$(VENV_NAME)/bin/activate: requirements.txt
	@echo "Setting up virtual environment..."
	@$(PYTHON) -m venv $(VENV_NAME)
	@. $(VENV_NAME)/bin/activate; pip install -r requirements.txt
	@echo "Virtual environment setup complete."

.PHONY: clean
clean:
	@echo "Cleaning up..."
	@rm -rf $(VENV_NAME)
	@echo "Cleanup complete."
