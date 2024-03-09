import environ
import os
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent.parent
env = environ.Env()
environ.Env.read_env()
SECRET_KEY = env("SECRET_KEY")
DEBUG = False
ALLOWED_HOSTS = ['*', 'http://127.0.0.1',
'https://vikinglockers.up.railway.app',]

CSRF_TRUSTED_ORIGINS = [
    'https://vikinglockers.up.railway.app',
    'http://127.0.0.1',
]
# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'base',    
    'import_export',
    # 'debug_toolbar',
    'rest_framework',
    'corsheaders',
]
AUTH_USER_MODEL = 'base.User'
# INTERNAL_IPS = ["127.0.0.1",] #debug toolbar
MIDDLEWARE = [
    # 'debug_toolbar.middleware.DebugToolbarMiddleware', ## tijdens debug 
    'django.middleware.security.SecurityMiddleware',
    "corsheaders.middleware.CorsMiddleware",  #29-10-2022
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    "whitenoise.middleware.WhiteNoiseMiddleware",  #29-10-22
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'vikinglockers.urls'
from django.contrib.messages import constants as messages
MESSAGE_TAGS = {
        messages.DEBUG: 'alert-secondary',
        messages.INFO: 'alert-info',
        messages.SUCCESS: 'alert-success',
        messages.WARNING: 'alert-warning',
        messages.ERROR: 'alert-danger',
}
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS':[ BASE_DIR / 'templates','base'
        ],
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

WSGI_APPLICATION = 'vikinglockers.wsgi.application'
# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = {
   'default': {
       'ENGINE': 'django.db.backends.postgresql',
       'NAME':env("DATABASE_NAME"), 
       'USER': env("DATABASE_USER"),
       'PASSWORD':env("DATABASE_PASS"),
       'HOST':'monorail.proxy.rlwy.net',
       'PORT': '58927'
   }
}
# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators
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


# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/
# do comment static root path

STATIC_ROOT = os.path.join(BASE_DIR, 'static')

# add static dirs path like this

STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]

#----------- OR ---------------

STATICFILES_DIRS = [BASE_DIR / 'staticfiles']

STATIC_URL = '/static/'
MEDIA_URL='/images/'
# if DEBUG:
#     STATICFILES_DIRS = [
#     os.path.join(BASE_DIR, 'static')]
# else:
#     STATIC_ROOT =     os.path.join(BASE_DIR, 'static')
#     MEDIA_ROOT =     os.path.join(BASE_DIR, 'media')
#     STATICFILES_DIRS = [
#     os.path.join(BASE_DIR, 'staticfiles')]
DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'
CORS_ALLOW_ALL_ORIGINS=True
SECURE_CONTENT_TYPE_NOSNIFF=False
# FIXTURE_DIRS = [BASE_DIR / 'static']
# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

