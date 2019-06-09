from .settings import *

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ['SECRET_KEY']

ALLOWED_HOSTS = ['.pythonanywhere.com']

FILE_UPLOAD_PERMISSIONS = 0o644
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True

# Database

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        'CONN_MAX_AGE': 3600,
    }
}
