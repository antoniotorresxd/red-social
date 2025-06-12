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
CORS_ALLOW_CREDENTIALS = True

CSRF_TRUSTED_ORIGINS = [
    f"https://{host}" for host in ALLOWED_HOSTS
]

CORS_ALLOWED_ORIGINS = [
    f"https://{host}" for host in ALLOWED_HOSTS
]

CORS_ORIGIN_WHITELIST = CORS_ALLOWED_ORIGINS

#  STATICS 
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'static'


# Azure Storage settings
AZURE_ACCOUNT_NAME = os.environ["AZURE_ACCOUNT_NAME"]
AZURE_ACCOUNT_KEY = os.environ["AZURE_ACCOUNT_KEY"]
AZURE_CONTAINER = os.environ.get("AZURE_CONTAINER", "media")

# Configuraciones adicionales críticas
AZURE_SSL = True
AZURE_UPLOAD_MAX_CONN = 2
AZURE_TIMEOUT = 30
AZURE_MAX_MEMORY_SIZE = 5*1024*1024  # 2MB

# Media URL
AZURE_CUSTOM_DOMAIN = f"{AZURE_ACCOUNT_NAME}.blob.core.windows.net"
MEDIA_URL = f"https://{AZURE_CUSTOM_DOMAIN}/{AZURE_CONTAINER}/"

# Para debugging temporal
AZURE_EMULATED = False