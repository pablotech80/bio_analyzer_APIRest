release: python run_migrations.py
web: gunicorn --bind 0.0.0.0:$PORT --workers 2 --threads 4 --timeout 60 run:app
