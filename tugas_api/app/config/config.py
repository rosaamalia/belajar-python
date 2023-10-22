import os
from datetime import timedelta
from decouple import config

BASE_DIR = os.path.dirname(os.path.realpath(__file__))

class Config:
    SECRET_KEY = config('SECRET_KEY', 'secret')
    JWT_SECRET_KEY = config('JWT_SECRET_KEY', 'rahasiabangeloo')
    DEBUG = config('DEBUG', cast=bool)
    SQLALCHEMY_TRACK_MODIFICATIONS = config('SQLALCHEMY_TRACK_MODIFICATIONS', cast=bool)
    SQLALCHEMY_ECHO = config('SQLALCHEMY_ECHO', cast=bool)

class Devconfig(Config):
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:''@localhost/course-online'
    SQLALCHEMY_RECORD_QUERIES = config('SQLALCHEMY_RECORD_QUERIES', cast=bool)
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=30)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)

class Qasconfig(Config):
    pass

class Prdconfig(Config):
    pass

config_dict = {
    'dev': Devconfig,
    'qas': Qasconfig,
    'prd': Prdconfig
}