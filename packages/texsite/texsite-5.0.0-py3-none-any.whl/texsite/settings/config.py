import os
from pathlib import Path


TEXSITE_DEBUG = os.environ.get('TEXSITE_DEBUG', 'False').lower() == 'true'
TEXSITE_DATA_ROOT = Path(os.environ.get('TEXSITE_DATA_ROOT', './.data'))
TEXSITE_ALLOWED_HOSTS = os.environ.get(
    'TEXSITE_ALLOWED_HOSTS', 'localhost'
).split(',')
TEXSITE_SECURE_PROXY = (
    os.environ.get('TEXSITE_SECURE_PROXY', 'False').lower() == 'true'
)
TEXSITE_SECRET_KEY = os.environ.get('TEXSITE_SECRET_KEY', '')

if not TEXSITE_DATA_ROOT.is_dir():
    raise ValueError('TEXSITE_DATA_ROOT must point to an existing directory')

if len(TEXSITE_SECRET_KEY) < 50:
    raise ValueError('TEXSITE_SECRET_KEY must be at least 50 characters long')

TEXSITE_DATABASE = {
    'ENGINE': 'django.db.backends.sqlite3',
    'NAME': str(TEXSITE_DATA_ROOT / 'db.sqlite3'),
}
