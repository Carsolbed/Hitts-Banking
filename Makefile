.PHONY: setup lint test deploy-dev

setup:
	python -m venv .venv && . .venv/bin/activate && pip install -e ".[dev]" && pre-commit install

lint:
	ruff check src tests && mypy src --ignore-missing-imports

test:
	pytest tests/unit -q

deploy-dev:
	cd pipelines && databricks bundle deploy -t dev
