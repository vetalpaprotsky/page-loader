install:
	poetry install

package-install:
	pip install --user dist/*.whl

test:
	poetry run pytest tests --cov=page_loader

lint:
	poetry run flake8 page_loader

selfcheck:
	poetry check

check: selfcheck test lint

build: check
	poetry build

publish-test:
	poetry publish -r test-pypi

.PHONY: install package-install test lint selfcheck check build publish-test
