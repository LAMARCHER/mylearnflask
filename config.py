# coding:utf-8
import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get('SECRET_EKY') or 'hard to guess string'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    FLASK_MAIL_SUBJECT_PREFIX = '[FLASKY]'
    FLASK_MAIL_SENDER = '13598508924@1139.com'
    FLASKY_ADMIN = os.environ.get('FLASKY_ADMIN')
    FLASK_POSTS_PER_PAGE = 10
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    MAIL_SERVER = 'smtp.139.com'
    MAIL_PORT = 25
    MAIL_USE_TLS = True
    MAIL_USER_NAME = '13598508974'
    MAIL_PASSWORD = 'LIU1028140200'


    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    MAIL_SERVER = 'smtp.139.com'
    MAIL_PORT = 25
    MAIL_USE_TLS = True
    MAIL_USERNAME = '13598508974'
    MAIL_PASSWORD = 'LIU1028140200'
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
