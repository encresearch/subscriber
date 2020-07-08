"""Configuration file containing the different configuration for our app."""
import os

BASEDIR = os.path.abspath(os.path.dirname(__file__))


class Config:
    """Base configuration."""
    DEBUG = False
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 465
    MAIL_USERNAME = 'encearthquakenotification@gmail.com'
    MAIL_DEFAULT_SENDER = MAIL_USERNAME
    MAIL_PASSWORD = "kohyomumdlonqmtq"
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True


class Dev(Config):
    """Configuration to be used in Dev environments."""
    SQLALCHEMY_DATABASE_URI = "postgresql://postgres:mysecretpassword@postgres:5432/enc_earthquake_email_list"
    SECRET_KEY = 'S@MpLe9SeCrEt#KeY'
    DEBUG = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    PRESERVE_CONTEXT_ON_EXCEPTION = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class Prod(Config):
    """Configuration to be used in production."""
    SQLALCHEMY_DATABASE_URI = 'sqlite://:memory:'


class Test(Dev):
    """Configuration to be used in testing environments."""
    SQLALCHEMY_DATABASE_URI = 'sqlite://'
    TESTING = True
