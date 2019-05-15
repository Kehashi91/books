"""
todo: add more valid config options (prod and testing)
"""

import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    # base

    WTF_CSRF_ENABLED = True
    SECRET_KEY = os.environ.get('SECRET_KEY') or '4142141rsaasfd;o3w485a;o8hnp'
    DB_PASS = os.environ.get('DB_PASS')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "postgresql://books:{}@localhost/books".format(Config.DB_PASS)
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True


config = {
    'development': DevelopmentConfig,
}
