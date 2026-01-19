# app/config.py
import os
from datetime import timedelta

from dotenv import load_dotenv

load_dotenv()


class Config:
    """Configuración base compartida por todos los entornos."""

    # Security
    SECRET_KEY = os.environ.get("SECRET_KEY") or "dev-secret-key-change-in-production"

    # Database
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = False

    # Flask-Login
    REMEMBER_COOKIE_DURATION = timedelta(days=7)
    REMEMBER_COOKIE_SECURE = True
    REMEMBER_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = "Lax"

    # JWT
    JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY") or SECRET_KEY
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)
    JWT_TOKEN_LOCATION = ["headers", "cookies"]
    JWT_COOKIE_SECURE = True
    JWT_COOKIE_CSRF_PROTECT = True

    # WTForms
    WTF_CSRF_ENABLED = True
    WTF_CSRF_TIME_LIMIT = None

    # AWS S3 Configuration
    AWS_ACCESS_KEY_ID = os.environ.get("AWS_ACCESS_KEY_ID")
    AWS_SECRET_ACCESS_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY")
    AWS_REGION = os.environ.get("AWS_REGION", "eu-north-1")
    S3_BUCKET = os.environ.get("S3_BUCKET")

    # Email (para futuro)
    MAIL_SERVER = os.environ.get("MAIL_SERVER")
    MAIL_PORT = int(os.environ.get("MAIL_PORT", 465))
    MAIL_USE_TLS = os.environ.get("MAIL_USE_TLS", "false").lower() == "true"
    MAIL_USE_SSL = os.environ.get("MAIL_USE_SSL", "true").lower() == "true"
    MAIL_USERNAME = os.environ.get("MAIL_USERNAME")
    MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD")
    MAIL_DEFAULT_SENDER = os.environ.get("MAIL_DEFAULT_SENDER")


class DevelopmentConfig(Config):
    """Configuración para desarrollo local."""

    DEBUG = True
    TESTING = False

    # SQLite para desarrollo
    SQLALCHEMY_DATABASE_URI = (
        os.environ.get("DEV_DATABASE_URL") or "sqlite:///coachbodyfit360_dev.db"
    )

    # Desactivar seguridad de cookies en desarrollo
    SESSION_COOKIE_SECURE = False
    REMEMBER_COOKIE_SECURE = False
    JWT_COOKIE_SECURE = False


class ProductionConfig(Config):
    """Configuración para producción (Railway)."""

    DEBUG = False
    TESTING = False

    # PostgreSQL de Railway - Usar red privada para evitar cargos de egress
    # Railway provee DATABASE_PRIVATE_URL automáticamente
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_PRIVATE_URL") or os.environ.get("DATABASE_URL")

    # Si Railway usa postgres:// en lugar de postgresql://
    if SQLALCHEMY_DATABASE_URI and SQLALCHEMY_DATABASE_URI.startswith("postgres://"):
        SQLALCHEMY_DATABASE_URI = SQLALCHEMY_DATABASE_URI.replace(
            "postgres://", "postgresql://", 1
        )

    # Logging
    SQLALCHEMY_ECHO = False
    
    # Permitir cookies sin HTTPS si FORCE_HTTPS está en False (para debugging)
    # En producción normal, Railway maneja SSL automáticamente
    FORCE_HTTPS = os.environ.get("FORCE_HTTPS", "true").lower() == "true"
    
    if not FORCE_HTTPS:
        # Modo debug para producción - solo usar si hay problemas con SSL
        SESSION_COOKIE_SECURE = False
        REMEMBER_COOKIE_SECURE = False
        JWT_COOKIE_SECURE = False


class TestingConfig(Config):
    """Configuración para tests."""

    TESTING = True
    DEBUG = True

    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"

    WTF_CSRF_ENABLED = False
    JWT_COOKIE_CSRF_PROTECT = False


# Diccionario para seleccionar config
config_by_name = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
    "testing": TestingConfig,
}
