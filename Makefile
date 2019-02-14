clean:
	find . -name '__pycache__' -exec rm -fr {} +
	find . -name '.pytest_cache' -exec rm -fr {} +
	find . -name '.mypy_cache' -exec rm -fr {} +

test:
	pytest

coverage: 
	pytest -x --cov=injectark tests/ --cov-report term-missing -s