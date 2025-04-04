import os
from .base import *
DEBUG = False
ADMINS = [
    ('Carlos HP', 'carlosgaelhp@gmail.com'),
 ]
ALLOWED_HOSTS = ['*']
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('POSTGRES_DB'),
        'USER': os.environ.get('POSTGRES_USER'),
        'PASSWORD': os.environ.get('POSTGRES_PASSWORD'),
        'HOST': 'db',
        'PORT': 5432,
    }
 }

# SECURE_SSL_REDIRECT = True  # Redirigir HTTP a HTTPS
# SESSION_COOKIE_SECURE = True  # Cookies solo a través de HTTPS
# CSRF_COOKIE_SECURE = True  # Cookies de CSRF solo a través de HTTPS
SECURE_BROWSER_XSS_FILTER = True  # Activar filtro XSS
SECURE_CONTENT_TYPE_NOSNIFF = True  # Prevenir esnifado de tipo de contenido