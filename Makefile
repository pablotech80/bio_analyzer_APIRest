# Define el nombre de tu entorno virtual
VENV_NAME = .venv

# Rutas de activación de entorno virtual y Python
PYTHON_PATH = $(shell which python3)

# Añadir el directorio bin del entorno virtual a PATH
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
