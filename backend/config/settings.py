import os

from dotenv import find_dotenv, load_dotenv
from pathlib import Path

load_dotenv(find_dotenv())

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.environ['SECRET_KEY']

DEBUG = os.environ['DEBUG']

ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS").split(' ')

# base
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

# packages
INSTALLED_APPS += [
    'rest_framework',
    'django_filters',
    'drf_spectacular',
]

# apps
INSTALLED_APPS += [
    'api.apps.ApiConfig',
    'users.apps.UsersConfig',
    'workouts.apps.WorkoutsConfig',
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

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'config.wsgi.application'


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

AUTH_USER_MODEL = 'users.User'

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


###########################
#  LOCALIZATION
###########################
LANGUAGE_CODE = 'ru'
TIME_ZONE = 'Europe/Moscow'
USE_I18N = True
USE_TZ = True


###########################
#  DJANGO REST FRAMEWORK
###########################
REST_FRAMEWORK = {
    # 'DEFAULT_PERMISSION_CLASSES': [
    #     'rest_framework.permissions.IsAuthenticatedOrReadOnly',
    # ],
    #
    # 'DEFAULT_AUTHENTICATION_CLASSES': [
    #     'rest_framework.authentication.TokenAuthentication',
    # ],
    #
    # 'DEFAULT_FILTER_BACKENDS': [
    #     'django_filters.rest_framework.DjangoFilterBackend',
    # ],
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
}
###########################
#  DRF Spectacular
###########################
SPECTACULAR_SETTINGS = {
    "TITLE": "WellCoach",
    "VERSION": "0.0.1",
    "SERVE_INCLUDE_SCHEMA": False,
    "SWAGGER_UI_SETTINGS": {
        "filter": True,
    },
    "COMPONENT_SPLIT_REQUEST": True
}
###########################
#  STATIC AND MEDIA
###########################
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'collected_static'

MEDIA_URL = '/media/'
MEDIA_ROOT = '/media'


DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
