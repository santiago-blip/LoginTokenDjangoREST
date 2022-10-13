from .base import *
# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

'''
POSTGRESQL
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'example',
        'USER': 'postgres',
        'PASSWORD': 'password123',
        'HOST': 'localhost',
    }
}
'''
STATIC_URL = 'static/'