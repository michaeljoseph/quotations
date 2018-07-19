VENV = venv/bin

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

lint:venv
	$(VENV)/flake8 transaction_importer tests
	$(VENV)/isort -rc -c transaction_importer tests
	$(VENV)/black -S --check transaction_importer tests

style:venv
	$(VENV)/isort -rc -y transaction_importer tests
	$(VENV)/black -S transaction_importer tests

test:venv
	$(VENV)/pytest

flask:venv ## Runs the hot-reloading Flask development server
	SQS_QUEUE_NAME=local_qp-ms-transaction-importer-standardiser \
	FLASK_APP=transaction_importer/api.py \
	FLASK_ENV=development \
	$(VENV)/flask run

help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) \
	| sort \
	| awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-16s\033[0m %s\n", $$1, $$2}'
