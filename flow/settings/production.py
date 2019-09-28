from .base import *

DEBUG = False

ALLOWED_HOSTS = ['167.71.235.193', 'api.theflowai.com']


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'flow-app',
        'USER': 'flow_admin',
        'PASSWORD': 'yxwr24BCqbh3bfM',
        'HOST': 'localhost',
        'PORT': '',
    }
}
