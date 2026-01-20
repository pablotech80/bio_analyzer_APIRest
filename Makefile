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
	python -m pytest

# Linting
lint:
	black .
	isort .
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
