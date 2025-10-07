release: flask db upgrade
web: gunicorn --bind 0.0.0.0:$PORT --workers 2 --threads 4 --timeout 60 run:app
