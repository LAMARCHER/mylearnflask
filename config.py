# coding:utf-8
import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get('SECRET_EKY') or 'lwb'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    FLASK_MAIL_SUBJECT_PREFIX = '[FLASKY]'
    FLASK_MAIL_SENDER = os.environ.get('MAIL_USER_NAME') + '@139.com'
    FLASKY_ADMIN = os.environ.get('FLASKY_ADMIN')
    FLASK_POSTS_PER_PAGE = 10
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    MAIL_SERVER = 'smtp.139.com'
    MAIL_PORT = 25
    MAIL_USE_TLS = True
    MAIL_USER_NAME = os.environ.get('MAIL_USER_NAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')


    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    MAIL_SERVER = 'smtp.139.com'
    MAIL_PORT = 25
    MAIL_USE_TLS = True
    MAIL_USER_NAME = os.environ.get('MAIL_USER_NAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    SQLALCHEMY_DATABASE_URI = 'mysql://root:123456@127.0.0.1:3306/test' or 'sqlite:///' + os.path.join(basedir, 'data-debug.sqlite')


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URI') or 'sqlite:///' + os.path.join(basedir, 'data-test.sqlite')


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI') or 'sqlite:///' + os.path.join(basedir, 'data.sqlite')


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,

    'default': DevelopmentConfig
}