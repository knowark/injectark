PROJECT = injectark
PART ?= patch

clean:
	find . -name '__pycache__' -exec rm -fr {} +
	find . -name '.pytest_cache' -exec rm -fr {} +
	find . -name '.mypy_cache' -exec rm -fr {} +

test:
	pytest

coverage:
	pytest -x --cov=$(PROJECT) tests/ --cov-report term-missing -s

push:
	git push && git push --tags

version:
	bump2version $(PART) pyproject.toml $(PROJECT)/__init__.py --tag --commit
