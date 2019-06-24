from .settings import *

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'jq=%ay()%2scm18hahu^@6!l^y3^e2!xy4s&=f-9qrq*9rkh+l'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['127.0.0.1']

# Database

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': str(BASE_DIR / 'db.sqlite3'),
    }
}
