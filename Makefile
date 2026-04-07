.PHONY: test lint format check run-debate

test:
	uv run pytest --cov=decision_prism --cov-report=term-missing

lint:
	uv run ruff check decision_prism tests

format:
	uv run ruff format decision_prism tests

type-check:
	uv run mypy decision_prism

check: lint type-check

run-debate:
	uv run decision-prism debate
