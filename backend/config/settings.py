import os

from datetime import timedelta
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
PASSWORD_MAX_LENGTH = 125
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
SPECIALIST_ROLE_CHOICES = (
        ('0', 'Client'),
        ('1', 'Trainer'),
        ('2', 'Nutritionist'),
    )
GENDER_CHOICES = (
        ('0', 'Absent'),
        ('1', 'Female'),
        ('2', 'Male'),
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
    'rest_framework_simplejwt',
    'rest_framework_simplejwt.token_blacklist',
]

# packages
INSTALLED_APPS += [
    'rest_framework',
    'django_filters',
    'drf_spectacular',
    "drf_standardized_errors",
    'djoser',
    'social_django',
    'corsheaders',
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
    'corsheaders.middleware.CorsMiddleware',
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

if os.getenv("DEVELOPMENT") == 'True':
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': os.getenv(
                'DB_ENGINE', default='django.db.backends.postgresql'),
            'NAME': os.getenv('DB_NAME', default='postgres'),
            'USER': os.getenv('POSTGRES_USER', default='postgres'),
            'PASSWORD': os.getenv('POSTGRES_PASSWORD', default='postgres'),
            'HOST': os.getenv('DB_HOST', default='localhost'),
            'PORT': os.getenv('DB_PORT', default='5432'),
        },
    }

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

LOGOUT_REDIRECT_URL = '/api/'

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
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.SessionAuthentication'],
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend'],
    "DEFAULT_SCHEMA_CLASS": "drf_standardized_errors.openapi.AutoSchema",
    "EXCEPTION_HANDLER": "drf_standardized_errors.handler.exception_handler",
}

###########################
#  DRF Spectacular
###########################
# with open("../common_errors.md") as f:
#     description = f.read()

SPECTACULAR_SETTINGS = {
    "TITLE": "WellCoach",
    "VERSION": "0.0.1",
    "SERVE_INCLUDE_SCHEMA": False,
    "SWAGGER_UI_SETTINGS": {
        "filter": True,
    },
    "COMPONENT_SPLIT_REQUEST": True,
    # "DESCRIPTION": description,
    "ENUM_NAME_OVERRIDES": {
        "ValidationErrorEnum": "drf_standardized_errors.openapi_serializers.ValidationErrorEnum.values",
        "ClientErrorEnum": "drf_standardized_errors.openapi_serializers.ClientErrorEnum.values",
        "ServerErrorEnum": "drf_standardized_errors.openapi_serializers.ServerErrorEnum.values",
        "ErrorCode401Enum": "drf_standardized_errors.openapi_serializers.ErrorCode401Enum.values",
        "ErrorCode403Enum": "drf_standardized_errors.openapi_serializers.ErrorCode403Enum.values",
        "ErrorCode404Enum": "drf_standardized_errors.openapi_serializers.ErrorCode404Enum.values",
        "ErrorCode405Enum": "drf_standardized_errors.openapi_serializers.ErrorCode405Enum.values",
        "ErrorCode406Enum": "drf_standardized_errors.openapi_serializers.ErrorCode406Enum.values",
        "ErrorCode415Enum": "drf_standardized_errors.openapi_serializers.ErrorCode415Enum.values",
        "ErrorCode429Enum": "drf_standardized_errors.openapi_serializers.ErrorCode429Enum.values",
        "ErrorCode500Enum": "drf_standardized_errors.openapi_serializers.ErrorCode500Enum.values",
    },
    "POSTPROCESSING_HOOKS": ["drf_standardized_errors.openapi_hooks.postprocess_schema_enums"]
}
###########################
#  DRF Standardizer Errors
###########################

DRF_STANDARDIZED_ERRORS = {
    "ALLOWED_ERROR_STATUS_CODES": ["400"]
}
###########################
#  STATIC AND MEDIA
###########################
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'collected_static'

MEDIA_URL = '/media/'
MEDIA_ROOT = '/app/media'

#########
#  Email
#########
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.yandex.ru'
EMAIL_PORT = 465
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')
EMAIL_USE_SSL = True
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
SERVER_EMAIL = EMAIL_HOST_USER
EMAIL_ADMIN = EMAIL_HOST_USER

##################################
#  Registration and authentication
##################################
AUTH_USER_MODEL = 'users.User'

STD_CLIENT_PASSWORD = os.getenv('STD_CLIENT_PASSWORD')

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

SIMPLE_JWT = {
    'AUTH_HEADER_TYPES': ('JWT',),
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=60),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
}

JWT_AUTH = {
    'JWT_RESPONSE_PAYLOAD_HANDLER':
    # 'rest_framework_jwt.utils.jwt_response_payload_handler',
    'users.utils.jwt_response_payload_handler',
}

DJOSER = {
    'LOGIN_FIELD': 'email',
    'HIDE_USERS': False,
    'USER_CREATE_PASSWORD_RETYPE': True,
    # 'SEND_ACTIVATION_EMAIL': True,
    # 'SEND_CONFIRMATION_EMAIL': True,
    'SET_PASSWORD_RETYPE': True,
    # 'ACTIVATION_URL': 'api/activate/{uid}/{token}',
    'SOCIAL_AUTH_TOKEN_STRATEGY': 'djoser.social.token.jwt.TokenStrategy',
    'SOCIAL_AUTH_ALLOWED_REDIRECT_URIS': [
        'https://connect.mail.ru',
        'http://localhost:8000/complete/yandex-oauth2/',
        'http://localhost:8000/complete/vk-oauth2/',
    ],
    'SERIALIZERS': {
        'user': 'api.serializers.CustomUserSerializer',
        'user_delete': 'api.serializers.CustomUserSerializer',
    },
    'PERMISSIONS': {
        'user': ('rest_framework.permissions.IsAuthenticated',),
        'user_delete': ('rest_framework.permissions.IsAuthenticated',),
    },
}

AUTHENTICATION_BACKENDS = (
    'social_core.backends.mailru.MailruOAuth2',
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


# CORS HEADERS
CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_CREDENTIALS = True
