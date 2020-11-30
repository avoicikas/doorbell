SHELL := /bin/bash

.PHONY: setup
setup:
	stat venv/bin/activate &> /dev/null || \
	virtualenv venv -p python3.6
	source venv/bin/activate; \
	pip install -r requirements.txt
.PHONY: run
run:
	source venv/bin/activate; \
	source env.sh; \
	python .bell\server.py
.PHONY: lint_ci
lint_ci:
	flake8 bell