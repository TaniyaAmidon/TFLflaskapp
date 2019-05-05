import os

class Config(object):
    ENV = os.environ.get('ENV', 'development')
    DEBUG = os.environ.get('DEBUG', True)
    DB_NAME = os.environ.get('DB_NAME', "tfl")
    DB_USER = os.environ.get('DB_USER')
    DB_HOST = os.environ.get('DB_HOST', "localhost")
    DB_PASS = os.environ.get('DB_PASS')