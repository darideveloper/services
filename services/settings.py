import os
import sys
from dotenv import load_dotenv

ENV = "prod"

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

# load environment variables
if ENV == "dev":
    print("running in dev environment")
    load_dotenv = load_dotenv(os.path.join(BASE_DIR, ".env.dev"))
elif ENV == "prod":
    print("running in prod environment")
    load_dotenv = load_dotenv(os.path.join(BASE_DIR, ".env.prod"))

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get("SECRET_KEY")
DEBUG = os.environ.get("DEBUG") == "True"

# Apps
INSTALLED_APPS = [
    "stripe_api",
    "contactform",
    "core",
    "blog",
    # 'ai',
    # 'activitywatch',
    "corsheaders",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",
    "rest_framework.authtoken",
]

MIDDLEWARE = [
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "services.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": ["templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
            "debug": DEBUG,
        },
    },
]

WSGI_APPLICATION = "services.wsgi.application"


# Database
IS_TESTING = len(sys.argv) > 1 and sys.argv[1] == "test"

if IS_TESTING:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": os.path.join(BASE_DIR, "testing.sqlite3"),
        }
    }
else:

    options = {}
    if os.environ.get("DB_ENGINE") == "django.db.backends.mysql":
        options = {
            "init_command": "SET sql_mode='STRICT_TRANS_TABLES'",
            "charset": "utf8mb4",
        }

    DATABASES = {
        "default": {
            "ENGINE": os.environ.get("DB_ENGINE"),
            "NAME": os.environ.get("DB_NAME"),
            "USER": os.environ.get("DB_USER"),
            "PASSWORD": os.environ.get("DB_PASSWORD"),
            "HOST": os.environ.get("DB_HOST"),
            "PORT": os.environ.get("DB_PORT"),
            "OPTIONS": options,
        }
    }


# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation"
        ".UserAttributeSimilarityValidator",
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


# Internationalization
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "America/Mexico_City"

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Allow all host headers
ALLOWED_HOSTS = ["*"]

STATIC_ROOT = os.path.join(PROJECT_ROOT, "staticfiles")
MEDIA_ROOT = os.path.join(BASE_DIR, "media")

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Simplified static file serving.
if DEBUG:
    STATICFILES_STORAGE = "django.contrib.staticfiles.storage.StaticFilesStorage"
else:
    STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# Emails
EMAIL_HOST = os.environ.get("EMAIL_HOST")
EMAIL_PORT = os.environ.get("EMAIL_PORT")
EMAIL_HOST_USER = os.environ.get("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = os.environ.get("EMAIL_HOST_PASSWORD")
EMAIL_USE_SSL = os.environ.get("EMAIL_USE_SSL") == "True"

FILE_UPLOAD_HANDLERS = [
    "django.core.files.uploadhandler.TemporaryFileUploadHandler",
]

if not DEBUG:
    SECURE_SSL_REDIRECT = True


CSRF_TRUSTED_ORIGINS = [
    "https://services.app.darideveloper.com",
    "https://services.darideveloper.com",
    "http://127.0.0.1:8000",
    "http://localhost:8000",
    "http://127.0.0.1:8000",
]

CORS_ALLOW_ALL_ORIGINS = True

REST_FRAMEWORK = {"EXCEPTION_HANDLER": "utils.handlers.custom_exception_handler"}

DATA_UPLOAD_MAX_MEMORY_SIZE = 50 * 1024 * 1024


# Storage settings
STORAGE_AWS = os.environ.get("STORAGE_AWS") == "True"
if STORAGE_AWS:
    # aws settings
    AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
    AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
    AWS_STORAGE_BUCKET_NAME = os.getenv("AWS_STORAGE_BUCKET_NAME")
    AWS_DEFAULT_ACL = None
    AWS_S3_CUSTOM_DOMAIN = f"{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com"
    AWS_S3_OBJECT_PARAMETERS = {"CacheControl": "max-age=86400"}

    # s3 static settings
    STATIC_LOCATION = "static"
    STATIC_URL = f"https://{AWS_S3_CUSTOM_DOMAIN}/{STATIC_LOCATION}/"
    STATICFILES_STORAGE = "services.storage_backends.StaticStorage"
    # s3 public media settings

    PUBLIC_MEDIA_LOCATION = "media"
    MEDIA_URL = f"https://{AWS_S3_CUSTOM_DOMAIN}/{PUBLIC_MEDIA_LOCATION}/"
    DEFAULT_FILE_STORAGE = "services.storage_backends.PublicMediaStorage"

    # s3 private media settings
    PRIVATE_MEDIA_LOCATION = "private"
    PRIVATE_FILE_STORAGE = "services.storage_backends.PrivateMediaStorage"

    # Disable Django's own staticfiles handling in favour of WhiteNoise
    # for greater consistency between gunicorn and
    STATIC_ROOT = None
    MEDIA_ROOT = None
else:
    # Local development (Windows or local server)
    STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")
    MEDIA_ROOT = os.path.join(BASE_DIR, "media")

    # Static files (CSS, JavaScript, Images)
    STATIC_URL = "/static/"
    MEDIA_URL = "/media/"
