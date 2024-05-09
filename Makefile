.PHONY: setup
.PHONY: build
.PHONY: lint
.PHONY: test

setup:
	@which python3 > /dev/null 2>&1 || (echo "Python is not installed on the system. Please install Python and try again." && exit 1)
	python3 -m venv .venv
	.venv/bin/pip install -r app/requirements.txt

build:
	@which docker > /dev/null 2>&1 || (echo "Docker is not installed on the system. Please install Docker and try again." && exit 1)
	docker build -t nadocast-ui .

lint:
	.venv/bin/ruff check app --fix
	.venv/bin/mypy --install-types
	.venv/bin/mypy app --ignore-missing-imports --config-file=pyproject.toml
	.venv/bin/black app

test:
	.venv/bin/pytest app