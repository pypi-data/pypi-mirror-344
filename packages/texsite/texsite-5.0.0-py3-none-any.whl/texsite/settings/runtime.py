from texsite.settings import config
from texsite.settings.base import *  # noqa: F401, F403


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config.TEXSITE_DEBUG

# SECURITY WARNING: define the correct values in production!
ALLOWED_HOSTS = config.TEXSITE_ALLOWED_HOSTS

if config.TEXSITE_SECURE_PROXY:
    # This is a reverse proxy setup, so we need to set the following
    # to ensure that Django knows it's behind a proxy.
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config.TEXSITE_SECRET_KEY

# Persistence settings
MEDIA_ROOT = config.TEXSITE_DATA_ROOT / 'media'
STATIC_ROOT = config.TEXSITE_DATA_ROOT / 'static'
DATABASES = {'default': config.TEXSITE_DATABASE}
