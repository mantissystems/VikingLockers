import environ
from .base import *  # noqa
env=environ.Env()
SECRET_KEY = 'django-insecure-)r2waboda$o)g39!ap!l7dx$numws6k7zi9=m*3e1hbudc!2&r'
# SECRET_KEY = env("SECRET_KEY")
DEBUG = True
INSTALLED_APPS = INSTALLED_APPS + ["django_extensions"]
INSTALLED_APPS = INSTALLED_APPS + ["debug_toolbar"]
MIDDLEWARE = MIDDLEWARE + ["debug_toolbar.middleware.DebugToolbarMiddleware"] 
INTERNAL_IPS = ["127.0.0.1",] #debug toolbar
ROOT_URLCONF = 'ploegenlijst.urls.dev.urls'