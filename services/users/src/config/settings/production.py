import os
from config.settings.base import *
import dj_database_url

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ['SECRET_KEY']

DEBUG = os.environ['DEBUG']

ALLOWED_HOSTS = os.environ['ALLOWED_HOSTS'].split(',')

DATABASES = {
    'default': dj_database_url.config(default=os.environ['DATABASE_DEFAULT'])
}

# CORS DjangoRest
# CORS_ALLOW_CREDENTIALS = True

# CSRF_TRUSTED_ORIGINS = [
#     f"https://{host}" for host in ALLOWED_HOSTS
# ]

# CORS_ALLOWED_ORIGINS = [
#     f"https://{host}" for host in ALLOWED_HOSTS
# ]

# CORS_ORIGIN_WHITELIST = CORS_ALLOWED_ORIGINS

#  STATICS 
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'static'

MEDIA_URL = '/media/'
MEDIA_ROOT =  BASE_DIR / 'media'