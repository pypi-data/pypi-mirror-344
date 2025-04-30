.PHONY: sort
sort: 
	isort .

.PHONY: format
format: 
	uv run ruff format

.PHONY: lint
lint:
	uv run ruff check

.PHONY: mypy
mypy: 
	uv run mypy .

.PHONY: qa
qa: sort format lint

.PHONY: test
test:
	uv run pytest

.PHONY: test-cov
test-cov:
	uv run pytest --cov=weblm --cov-report=term

.PHONY: test-cov-html
test-cov-html:
	uv run pytest --cov=weblm --cov-report=html