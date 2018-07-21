VENV = venv/bin
FILES = quotes.py tests.py
.DEFAULT_GOAL := generate

.PHONY: all help
all: test

.PHONY: clean-pyc
clean: ## Remove Python file artifacts and virtualenv
	@echo "+ $@"
	@find . -type d -name '__pycache__' -exec rm -rf {} +
	@find . -type f -name '*.py[co]' -exec rm -f {} +
	@find . -name '*~' -exec rm -f {} +
	@rm -rf venv

venv: ## Creates the virtualenv and installs requirements
	python3 -m venv venv
	$(VENV)/pip install -Ur requirements-dev.txt

requirements: ## Updates venv from requirements
	$(VENV)/pip install -Ur requirements-dev.txt

lint:venv
	$(VENV)/flake8 $(FILES)
	$(VENV)/isort -rc -c $(FILES)
	$(VENV)/black -S --check $(FILES)

style:venv
	$(VENV)/isort -rc -y $(FILES)
	$(VENV)/black -S $(FILES)

test:venv
	$(VENV)/pytest

generate:venv ## Runs the hot-reloading Flask development server
	$(VENV)/python quotes.py

help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) \
	| sort \
	| awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-16s\033[0m %s\n", $$1, $$2}'
