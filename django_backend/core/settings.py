"""
Django settings for CoachBodyFit360 Backend.

Multi-tenant SaaS platform for biometric analysis, nutrition, and training.
Designed for deployment on Azure with production-ready configurations.
"""

import os
from pathlib import Path
from decouple import config, Csv
import dj_database_url

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# ==============================================================================
# CORE SETTINGS
# ==============================================================================

SECRET_KEY = config('DJANGO_SECRET_KEY', default='django-insecure-dev-key-change-in-production')

DEBUG = config('DJANGO_DEBUG', default=True, cast=bool)

ALLOWED_HOSTS = config('DJANGO_ALLOWED_HOSTS', default='localhost,127.0.0.1', cast=Csv())

ENVIRONMENT = config('DJANGO_ENVIRONMENT', default='development')

# ==============================================================================
# APPLICATION DEFINITION
# ==============================================================================

INSTALLED_APPS = [
    # Django core apps
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # Third-party apps
    'rest_framework',
    'rest_framework_simplejwt',
    'corsheaders',
    'drf_spectacular',
    
    # Local apps
    'apps.users',
    'apps.organizations',
    'apps.permissions',
    'apps.bioanalyze',
    'apps.nutrition',
    'apps.training',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # Static files in production
    'corsheaders.middleware.CorsMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'core.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'core.wsgi.application'

# ==============================================================================
# DATABASE
# ==============================================================================

# Default to SQLite for development
DATABASES = {
    'default': dj_database_url.config(
        default=f'sqlite:///{BASE_DIR / "db.sqlite3"}',
        conn_max_age=600,
        conn_health_checks=True,
    )
}

# ==============================================================================
# AUTHENTICATION
# ==============================================================================

AUTH_USER_MODEL = 'users.User'

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {
            'min_length': 8,
        }
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Password hashing
PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.Argon2PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher',
    'django.contrib.auth.hashers.BCryptSHA256PasswordHasher',
]

# ==============================================================================
# REST FRAMEWORK & API
# ==============================================================================

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20,
    'DEFAULT_FILTER_BACKENDS': [
        'rest_framework.filters.SearchFilter',
        'rest_framework.filters.OrderingFilter',
    ],
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
    ],
    'DEFAULT_PARSER_CLASSES': [
        'rest_framework.parsers.JSONParser',
        'rest_framework.parsers.MultiPartParser',
        'rest_framework.parsers.FormParser',
    ],
    'EXCEPTION_HANDLER': 'rest_framework.views.exception_handler',
    'NON_FIELD_ERRORS_KEY': 'error',
    'DATETIME_FORMAT': '%Y-%m-%dT%H:%M:%S%z',
}

# ==============================================================================
# JWT SETTINGS
# ==============================================================================

from datetime import timedelta

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=config('JWT_ACCESS_TOKEN_LIFETIME_MINUTES', default=60, cast=int)),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=config('JWT_REFRESH_TOKEN_LIFETIME_DAYS', default=30, cast=int)),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
    'UPDATE_LAST_LOGIN': True,
    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY,
    'VERIFYING_KEY': None,
    'AUTH_HEADER_TYPES': ('Bearer',),
    'AUTH_HEADER_NAME': 'HTTP_AUTHORIZATION',
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',
    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
    'TOKEN_TYPE_CLAIM': 'token_type',
}

# ==============================================================================
# CORS SETTINGS
# ==============================================================================

CORS_ALLOWED_ORIGINS = config(
    'CORS_ALLOWED_ORIGINS',
    default='http://localhost:3000,http://localhost:5173',
    cast=Csv()
)

CORS_ALLOW_CREDENTIALS = True

CORS_ALLOW_METHODS = [
    'DELETE',
    'GET',
    'OPTIONS',
    'PATCH',
    'POST',
    'PUT',
]

CORS_ALLOW_HEADERS = [
    'accept',
    'accept-encoding',
    'authorization',
    'content-type',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
]

# ==============================================================================
# INTERNATIONALIZATION
# ==============================================================================

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

# ==============================================================================
# STATIC FILES (CSS, JavaScript, Images)
# ==============================================================================

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [BASE_DIR / 'static']

# WhiteNoise configuration for serving static files in production
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# ==============================================================================
# MEDIA FILES (User uploads)
# ==============================================================================

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# ==============================================================================
# AZURE STORAGE (Production)
# ==============================================================================

# Azure Blob Storage for media files in production
if ENVIRONMENT == 'production':
    AZURE_ACCOUNT_NAME = config('AZURE_STORAGE_ACCOUNT_NAME', default='')
    AZURE_ACCOUNT_KEY = config('AZURE_STORAGE_ACCOUNT_KEY', default='')
    AZURE_CONTAINER = config('AZURE_STORAGE_CONTAINER_NAME', default='media')
    
    if AZURE_ACCOUNT_NAME and AZURE_ACCOUNT_KEY:
        DEFAULT_FILE_STORAGE = 'storages.backends.azure_storage.AzureStorage'
        AZURE_CUSTOM_DOMAIN = f'{AZURE_ACCOUNT_NAME}.blob.core.windows.net'
        MEDIA_URL = f'https://{AZURE_CUSTOM_DOMAIN}/{AZURE_CONTAINER}/'

# ==============================================================================
# EMAIL CONFIGURATION
# ==============================================================================

EMAIL_BACKEND = config(
    'EMAIL_BACKEND',
    default='django.core.mail.backends.console.EmailBackend'
)

if ENVIRONMENT == 'production':
    EMAIL_HOST = config('EMAIL_HOST', default='')
    EMAIL_PORT = config('EMAIL_PORT', default=587, cast=int)
    EMAIL_USE_TLS = config('EMAIL_USE_TLS', default=True, cast=bool)
    EMAIL_HOST_USER = config('EMAIL_HOST_USER', default='')
    EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD', default='')
    DEFAULT_FROM_EMAIL = config('DEFAULT_FROM_EMAIL', default='noreply@coachbodyfit360.com')

# ==============================================================================
# AZURE OPENAI CONFIGURATION
# ==============================================================================

AZURE_OPENAI_ENDPOINT = config('AZURE_OPENAI_ENDPOINT', default='')
AZURE_OPENAI_API_KEY = config('AZURE_OPENAI_API_KEY', default='')
AZURE_OPENAI_DEPLOYMENT_NAME = config('AZURE_OPENAI_DEPLOYMENT_NAME', default='gpt-4o')
AZURE_OPENAI_API_VERSION = config('AZURE_OPENAI_API_VERSION', default='2024-02-15-preview')

# ==============================================================================
# LOGGING
# ==============================================================================

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname} {message}',
            'style': '{',
        },
    },
    'filters': {
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
    },
    'handlers': {
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': BASE_DIR / 'logs' / 'django.log',
            'formatter': 'verbose',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'file'] if ENVIRONMENT == 'production' else ['console'],
            'level': 'INFO',
            'propagate': False,
        },
        'apps': {
            'handlers': ['console', 'file'] if ENVIRONMENT == 'production' else ['console'],
            'level': 'DEBUG' if DEBUG else 'INFO',
            'propagate': False,
        },
    },
}

# Create logs directory if it doesn't exist
(BASE_DIR / 'logs').mkdir(exist_ok=True)

# ==============================================================================
# SECURITY SETTINGS
# ==============================================================================

if ENVIRONMENT == 'production':
    # HTTPS/SSL
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    X_FRAME_OPTIONS = 'DENY'
    
    # HSTS
    SECURE_HSTS_SECONDS = 31536000  # 1 year
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
    
    # Proxy headers
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# ==============================================================================
# API DOCUMENTATION (drf-spectacular)
# ==============================================================================

SPECTACULAR_SETTINGS = {
    'TITLE': 'CoachBodyFit360 API',
    'DESCRIPTION': 'Multi-tenant SaaS platform for biometric analysis, nutrition, and training',
    'VERSION': '1.0.0',
    'SERVE_INCLUDE_SCHEMA': False,
    'COMPONENT_SPLIT_REQUEST': True,
    'SCHEMA_PATH_PREFIX': r'/api/v[0-9]',
}

# ==============================================================================
# DEFAULT PRIMARY KEY FIELD TYPE
# ==============================================================================

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# ==============================================================================
# CUSTOM SETTINGS
# ==============================================================================

# Maximum file upload size (100MB for videos)
DATA_UPLOAD_MAX_MEMORY_SIZE = 104857600  # 100MB

# Session settings
SESSION_COOKIE_AGE = 1209600  # 2 weeks
SESSION_SAVE_EVERY_REQUEST = False

# Admin site customization
ADMIN_SITE_HEADER = 'CoachBodyFit360 Administration'
ADMIN_SITE_TITLE = 'CoachBodyFit360 Admin'
ADMIN_INDEX_TITLE = 'Welcome to CoachBodyFit360 Administration'
