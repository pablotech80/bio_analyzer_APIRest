import os

import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.local")
os.environ.setdefault("ALLOWED_HOSTS", "localhost,testserver")
django.setup()
