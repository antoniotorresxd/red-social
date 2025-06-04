import os

from config.settings.base import *
from dotenv import load_dotenv

load_dotenv(Path.joinpath(BASE_DIR, '.env'))

import dj_database_url

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['red-social.up.railway.app']

# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

DATABASES = {'default': dj_database_url.config(default=os.environ.get('DATABASE_DEFAULT'))}


CSRF_TRUSTED_ORIGINS = [
    'https://red-social.up.railway.app/', 
]


# Cors DjangoRest

CORS_ALLOW_CREDENTIALS = True

CORS_ALLOWED_ORIGINS = [
    "https://red-social.up.railway.app", 
]

CORS_ORIGIN_WHITELIST = [
    "https://red-social.up.railway.app",
]