web: gunicorn --bind 0.0.0.0:$PORT --workers 2 --threads 4 --timeout 60 --access-logfile - --error-logfile - run:app
release: flask db upgrade




