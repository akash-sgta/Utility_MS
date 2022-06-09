# =========================================================================================
#                                       DOCUMENTATION
# =========================================================================================
"""
Django settings for utility project.

Generated by 'django-admin startproject' using Django 4.0.1.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.0/ref/settings/
"""

# =========================================================================================
#                                       LIBRARY
# =========================================================================================
from pathlib import Path
import os
import json
from schemadict import schemadict

# =========================================================================================
#                                       CONSTANT
# =========================================================================================
from utilData.key import *

# --------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent.parent

try:
    with open(os.path.join(BASE_DIR, "utilData", "keys.json"), "r") as secret:
        json_secret = json.load(secret)
        if not validateKey(json_secret=json_secret):
            raise Exception("INVALID KEY FILE")
        SECRET_KEY = json_secret[K_SYSTEM][K_SECRET_KEY]
        DEBUG = json_secret[K_SYSTEM][K_DEBUG]
        ALLOWED_HOSTS = json_secret[K_SYSTEM][K_ALLOWED_HOSTS]
        SYSTEM = json_secret[K_SYSTEM][K_ID]
        SERVER_NAME = json_secret[K_SYSTEM][K_NAME]
        EMAIL_HOST_USER = json_secret[K_ADMIN][K_EMAIL][K_HOST_USER]
        EMAIL_HOST_PASSWORD = json_secret[K_ADMIN][K_EMAIL][K_HOST_PASSWORD]
        EMAIL_HOST_PORT = json_secret[K_ADMIN][K_EMAIL][K_HOST_PORT]
        TELEGRAM_NAME = json_secret[K_ADMIN][K_EMAIL][K_NAME]
        TELEGRAM_KEY = json_secret[K_ADMIN][K_EMAIL][K_KEY]
        del json_secret
except Exception as e:
    print(f"ERROR : {str(e)}")
    exit()

try:
    os.mkdir(os.path.join(BASE_DIR, "staticfiles"))
except Exception as e:
    print(f"ERROR : {str(e)}")

# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # ------------------------------------------------------------------------
    "utilUtilities",
    "utilApi",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    # ------------------------------------------------------------------------
    "corsheaders.middleware.CorsMiddleware",
]

ROOT_URLCONF = "utility.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            os.path.join(BASE_DIR, "templates"),
        ],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "utility.wsgi.application"

# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

DB_PATH = os.path.join(BASE_DIR, "utilData", "db.sqlite3")
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": DB_PATH,
    }
}

# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Internationalization
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = "en-us"
USE_TZ = True
TIME_ZONE = "Asia/Kolkata"
USE_I18N = True

STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "static")
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "staticfiles"),
]
MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")
DATA_UPLOAD_MAX_MEMORY_SIZE = 1048576 * 10  # 10MB

CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOW_HEADERS = [
    "accept",
    "accept-encoding",
    "dnt",
    "origin",
    "user-agent",
    "x-csrftoken",
    "x-requested-with",
    # -----------------------------------------------------------------------
    "authorization",
    "content-type",
    "Access-Control-Allow-Origin",
]

# DATABASE_ROUTERS = (
#     "databases.auth.Django_Auth_Router",
#     "databases.app.App_Router",
# )

REFRESH_TOKEN_LIMIT = (7, "D")
REFRESH_TOKEN_LEN = 255
ACCESS_TOKEN_LIMIT = (120, "m")
ACCESS_TOKEN_LEN = 127

REST_FRAMEWORK = {
    "DEFAULT_PERMISSION_CLASSES": ["rest_framework.permissions.AllowAny"]
}
# =========================================================================================
#                                       CODE
# =========================================================================================
