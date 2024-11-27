
from datetime import timedelta
from pathlib import Path
import os
#from api_heaven.serializers import IntegerFieldSerializer

BASE_DIR = Path(__file__).resolve().parent.parent

AUTH_USER_MODEL = 'api_heaven.CustomUser'

SECRET_KEY = 'django-insecure-)!j8ddu#p0r%(_zd$+li%ru86n(e&16wat-7i)a-@7z!7p62z%'

DEBUG = True

ALLOWED_HOSTS = []


INSTALLED_APPS = [
    
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    "rest_framework",
    "api_heaven.apps.ApiHeavenConfig",
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

ROOT_URLCONF = 'track_life_back.urls'

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

WSGI_APPLICATION = 'track_life_back.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

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

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
}

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(days=1),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=1),
}

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

STATIC_URL = 'static/'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# URL to access media files
MEDIA_URL = '/media/'

# Directory on the server where media files will be stored
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')


FLEX_TABLE_STRUCTURE={
    "type":{

        "integer":{
            "serializer":"api_heaven.serializers.IntegerFieldSerializer",
            "pre_save":None,
            "pre_update":None,
            "required_parameter":None
        },

        "text":{
            "serializer":"api_heaven.serializers.TextFieldSerializer",
            "pre_save":None,
            "pre_update":None,
            "required_parameter":None
        },

        "date":{
            "serializer":"api_heaven.serializers.DateFieldSerializer",
            "pre_save":None,
            "pre_update":None,
            "required_parameter":None
        },

        "image":{
            "serializer":"api_heaven.serializers.ImageFieldSerializer",
            "pre_save":"api_heaven.db_operation_helper.image_post_process",
            "pre_update":"api_heaven.db_operation_helper.delete_old_file",
            "required_parameter":None
        }


    }
}
