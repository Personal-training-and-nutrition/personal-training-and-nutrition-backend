import os

from dotenv import find_dotenv, load_dotenv
from pathlib import Path

# Global constants
OTHER_MAX_LENGTH = 128
TEXT_MAX_LENGTH = 300
NAME_MAX_LENGTH = 50
NAME_MIN_LENGTH = 2
PHONE_MAX_LENGTH = 15
PHONE_MIN_LENGTH = 9
EMAIL_MAX_LENGTH = 50
EMAIL_MIN_LENGTH = 5
PASSWORD_MIN_LENGTH = 8
PASSWORD_MAX_LENGTH = 25
KKAL_MAX_PER_DAY = 10000
PROTEIN_MAX_PER_DAY = 500
CARBO_MAX_PER_DAY = 1000
FAT_MAX_PER_DAY = 300

WEEKDAY_CHOICES = (
    ('1', 'Понедельник'),
    ('2', 'Вторник'),
    ('3', 'Среда'),
    ('4', 'Четверг'),
    ('5', 'Пятница'),
    ('6', 'Суббота'),
    ('7', 'Воскресенье'),
)


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
    'rest_framework.authtoken',
]

# packages
INSTALLED_APPS += [
    'rest_framework',
    'django_filters',
    'drf_spectacular',
    'djoser',
    'social_django',
]

# apps
INSTALLED_APPS += [
    'api.apps.ApiConfig',
    'diets.apps.DietsConfig',
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
                'social_django.context_processors.backends',
                'social_django.context_processors.login_redirect',
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
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True


###########################
#  DJANGO REST FRAMEWORK
###########################
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES':
        ('rest_framework.permissions.IsAuthenticated',),
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.SessionAuthentication'],
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend'],
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

LOGOUT_REDIRECT_URL = '/api/'

#########
#  Email
#########
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.mail.ru'
EMAIL_PORT = 465
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')
EMAIL_USE_SSL = True

##################################
#  Registration and authentication
##################################
DJOSER = {
    'LOGIN_FIELD': 'email',
    'HIDE_USERS': False,
    'USER_CREATE_PASSWORD_RETYPE': True,
    'SEND_ACTIVATION_EMAIL': True,
    'SEND_CONFIRMATION_EMAIL': True,
    'PASSWORD_RESET_SHOW_EMAIL_NOT_FOUND': True,
    'PASSWORD_RESET_CONFIRM_URL': True,
    'SET_PASSWORD_RETYPE': True,
    'ACTIVATION_URL': True,
    'PASSWORD_RESET_CONFIRM_RETYPE': True,
    'SERIALIZERS': {
        'user': 'api.serializers.UsersSerializer',
        'set_password': 'api.serializers.SetPasswordSerializer',
        'user_delete': 'api.serializers.UsersSerializer',
        'activation': 'djoser.email.ActivationEmail',
    },
    'PERMISSIONS': {
        'user': ('rest_framework.permissions.IsAuthenticated',),
        'user_delete': ('rest_framework.permissions.IsAuthenticated',),
    },
}

AUTHENTICATION_BACKENDS = (
    'social_core.backends.mailru.MRGOAuth2',
    'social_core.backends.vk.VKOAuth2',
    'social_core.backends.yandex.YandexOAuth2',
    'django.contrib.auth.backends.ModelBackend',
)

SOCIAL_AUTH_URL_NAMESPACE = 'social'
SOCIAL_AUTH_REQUIRE_POST = True

SOCIAL_AUTH_MAILRU_KEY = os.getenv('SOCIAL_AUTH_MAILRU_KEY')
SOCIAL_AUTH_MAILRU_SECRET = os.getenv('SOCIAL_AUTH_MAILRU_SECRET')
SOCIAL_AUTH_VK_OAUTH2_KEY = os.getenv('SOCIAL_AUTH_VK_OAUTH2_KEY')
SOCIAL_AUTH_VK_OAUTH2_SECRET = os.getenv('SOCIAL_AUTH_VK_OAUTH2_SECRET')
SOCIAL_AUTH_YANDEX_KEY = os.getenv('SOCIAL_AUTH_YANDEX_KEY')
SOCIAL_AUTH_YANDEX_SECRET = os.getenv('SOCIAL_AUTH_YANDEX_SECRET')
