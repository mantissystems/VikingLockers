# import environ
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
# env=environ.Env()

SECRET_KEY = 'django-insecure-)r2waboda$o)g39!ap!l7dx$numws6k7zi9=m*3e1hbudc!2&r'
DEBUG = True
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
    'viking',
    'base',
    
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
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'viking.sqlite3',
#     }
# }

DATABASES = {
   'default': {
       'ENGINE': 'django.db.backends.postgresql',
       'NAME': 'railway',
       'USER': 'postgres',
       'PASSWORD':'V0CRWmkgvstecDD07V1i',
       'HOST':'containers-us-west-135.railway.app',
       'PORT': '7980'
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

STATIC_URL = '/static/'
MEDIA_URL='/images/'
# STATICFILES_DIRS = [
# BASE_DIR / 'mykluisjes/build/static']

STATIC_ROOT = BASE_DIR.joinpath('staticfiles')
DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'
MEDIA_ROOT= BASE_DIR / 'static/images'
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
CORS_ALLOW_ALL_ORIGINS=True
SECURE_CONTENT_TYPE_NOSNIFF=False

# CORS_ALLOWED_ORIGINS = [
#     "http://*", 
#     "https://kluisjeslijst.up.railway.app",
#     "http://127.0.0.1",
#     "http://127.0.0.1:8000",
#     ]
# CORS_ALLOWED_ORIGIN_REGEXES= [r"https://",r"http://"]

# FIXTURE_DIRS = [BASE_DIR / 'static']
# SENDGRID_API_KEY = os.getenv('SENDGRID_API_KEY')

# EMAIL_HOST = 'smtp.sendgrid.net'
# EMAIL_HOST_USER = 'apikey' # this is exactly the value 'apikey'
# EMAIL_HOST_PASSWORD = SENDGRID_API_KEY
# EMAIL_PORT = 587
# EMAIL_USE_TLS = True
# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

