# Nombre del entorno virtual
VENV_NAME = venv1

# Ruta del ejecutable de Python del sistema
PYTHON_PATH = $(shell which python3)

# Añadir el directorio bin del entorno virtual al PATH
export PATH := /app/.local/bin:$(PATH)

# Crear entorno virtual
create-venv: delete-venv
	$(PYTHON_PATH) -m venv $(VENV_NAME)

# Eliminar entorno virtual
delete-venv:
	rm -rf $(VENV_NAME)

# Desinstalar proyecto
uninstall:
	$(VENV_NAME)/bin/pip uninstall -y body-analyzer

# Construir proyecto
build:
	$(PYTHON_PATH) -m build

# Limpiar directorios del proyecto
clean:
	rm -rf build dist *.egg-info
	find . -type d -name "__pycache__" -exec rm -r {} +
	find . -type f -name "*.pyc" -delete

# Reinstalar dependencias
reinstall-dependencies: delete-dependencies install-dep clean

# Actualizar pip
update-pip:
	$(VENV_NAME)/bin/python -m pip install --upgrade pip

# Eliminar todas las dependencias instaladas
delete-dependencies:
	$(VENV_NAME)/bin/pip freeze | xargs $(VENV_NAME)/bin/pip uninstall -y

# Instalar dependencias del proyecto
install-dep:
	$(VENV_NAME)/bin/pip install -e .

# Ejecutar la aplicación Flask
run:
	@if [ -d "$(VENV_NAME)" ]; then \
		FLASK_APP=run.py $(VENV_NAME)/bin/flask run --host=0.0.0.0 --port=5000; \
	else \
		FLASK_APP=run.py flask run --host=0.0.0.0 --port=5000; \
	fi

# Ejecutar pruebas
test:
	$(VENV_NAME)/bin/pytest

# Ejecutar pruebas del legado Flask (aisladas)
flask-test:
	$(VENV_NAME)/bin/pytest tests_flask

# Formatear código (repara estilo automáticamente)
format:
	$(VENV_NAME)/bin/isort .
	$(VENV_NAME)/bin/black .

# Lint (usable también en CI)
lint:
	black --check .
	isort --check .
	flake8

# CI/CD
ci:
	make lint
	make test

# -------------------------------------------------------------------------
# Django (migración) - targets separados para no romper Flask
# -------------------------------------------------------------------------
dj-run:
	python manage.py runserver 0.0.0.0:8000

dj-check:
	python manage.py check

dj-migrate:
	python manage.py migrate

dj-makemigrations:
	python manage.py makemigrations

dj-collectstatic:
	python manage.py collectstatic --no-input
