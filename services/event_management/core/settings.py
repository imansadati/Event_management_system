from pathlib import Path
import os
from grpc_service.client.client import RemoteUserClient
from datetime import timedelta

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure--_l+nk(-%chf(qz%e*rarg*a6$q-6*wdq+oo2zxo%_ljq2132z'


DJANGO_ENV = os.getenv("DJANGO_ENV", "development").strip().lower()

if DJANGO_ENV == "development":
    DEBUG = True
elif DJANGO_ENV == "production":
    DEBUG = False
else:
    raise ValueError(
        f"Invalid DJANGO_ENV: {DJANGO_ENV}. Must be 'development' or 'production'.")


ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS').split(',')


THIRD_PARTY_APPS = [
    'rest_framework',
    'rest_framework_simplejwt',
]

LOCAL_APPS = [
    'apps.events.apps.EventsConfig',
    'apps.organizer.apps.OrganizerConfig',
    'apps.venue.apps.VenueConfig',
    'apps.speaker.apps.SpeakerConfig',
    'apps.session.apps.SessionConfig',
]

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    *THIRD_PARTY_APPS,
    *LOCAL_APPS,
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
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
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'core.wsgi.application'

# Database
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('DB_NAME', 'event_postgres'),
        'USER': os.getenv('DB_USER', 'event_postgres'),
        'PASSWORD': os.getenv('DB_PASSWORD', 'event_postgres'),
        'HOST': os.getenv('DB_HOST', 'event_management_db'),
        'PORT': os.getenv('DB_PORT', '5432'),
    }
}

# Password validation
# https://docs.djangoproject.com/en/5.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

STATIC_URL = 'static/'
MEDIA_URL = 'media/'

STATIC_ROOT = '/app/static'
MEDIA_ROOT = '/app/media'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


JWT_ROLE_MODEL_MAP = {
    'attendee': RemoteUserClient,
    'staff': RemoteUserClient,
    'admin': RemoteUserClient,
}

REST_FRAMEWORK = {
    'EXCEPTION_HANDLER': 'shared_utils.exception.exception_handler.custom_exception_handler',
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'shared_utils.jwt_authentication.CustomJWTAuthentication',
    ),
}

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=30),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=7),
    "AUTH_HEADER_TYPES": ("Bearer",),
}

CELERY_BROKER_URL = os.environ.get(
    "CELERY_BROKER_URL", "amqp://guest:guest@rabbitmq:5672/")
CELERY_ACCEPT_CONTENT = ["json"]
CELERY_TASK_SERIALIZER = "json"
CELERY_RESULT_SERIALIZER = "json"
CELERY_TIMEZONE = "UTC"
CELERY_ENABLE_UTC = True
