import os

from .base import *  # noqa: F403

DEBUG = False

# Prefer DATABASE_URL in production (e.g. Railway/Render)
DATABASE_URL = os.environ.get("DATABASE_URL")
if DATABASE_URL:
    # Minimal parser for postgres URLs (keeps dependencies light)
    # Expected: postgres://user:pass@host:port/dbname
    url = DATABASE_URL.replace("postgresql://", "postgres://")
    if url.startswith("postgres://"):
        url = url[len("postgres://") :]
        creds, rest = url.split("@", 1)
        user, password = creds.split(":", 1)
        hostport, dbname = rest.split("/", 1)
        host, port = hostport.split(":", 1) if ":" in hostport else (hostport, "5432")
        DATABASES = {
            "default": {
                "ENGINE": "django.db.backends.postgresql",
                "NAME": dbname,
                "USER": user,
                "PASSWORD": password,
                "HOST": host,
                "PORT": port,
            }
        }
