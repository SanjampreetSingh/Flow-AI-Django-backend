from .base import *

DEBUG = True

ALLOWED_HOSTS = ['api.theflowai.com', 'localhost']


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


REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.DjangoModelPermissions',
    ),
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_jwt.authentication.JSONWebTokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
        'oauth2_provider.contrib.rest_framework.OAuth2Authentication',
        'rest_framework_social_oauth2.authentication.SocialAuthentication',
    ),
}


CORS_ORIGIN_ALLOW_ALL = False
CORS_ORIGIN_WHITELIST = [
    'https://theflowai.com',
    'https://www.theflowai.com',
    'https://flow-fe.kmvsingh007.now.sh'
]

# SENDGRID_API_KEY = "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"
# EMAIL_HOST = 'smtp.mailtrap.io'
# EMAIL_HOST_USER = 'afe9d617378e04'
# EMAIL_HOST_PASSWORD = '8b6846f7bfb7cc'
# EMAIL_PORT = '2525'
