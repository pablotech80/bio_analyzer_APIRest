# Django Commands
run:
	django-admin runserver 0.0.0.0:8000

migrate:
	django-admin migrate

makemigrations:
	django-admin makemigrations

collectstatic:
	django-admin collectstatic --no-input

# Testing
test:
	pytest

coverage:
	pytest --cov=.

# Linting
lint:
	black --check .
	isort --check .
	flake8

# Database
dbshell:
	django-admin dbshell

# Virtual Environment
venv:
	python -m venv venv
	./venv/bin/pip install -r requirements.txt

# CI/CD
ci:
	make lint
	make test
	make test
