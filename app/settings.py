import os

class BaseConfig(object):
    DEBUG = False
    CSRF_ENABLED = True
    SECRET_KEY = os.getenv('SECRET', 'default_secret_key')
    ACCESS_TOKEN_AGE = 1
    REFRESH_TOKEN_AGE = 10

class DevelopmentConfig(BaseConfig):
    DEBUG = True