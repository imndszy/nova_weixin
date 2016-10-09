# -*- coding:utf8 -*- 
# Author: shizhenyu96@gamil.com
# github: https://github.com/imndszy
import os
basedir = os.path.abspath(os.path.dirname(__file__))

ROOT_USER = 'nova_cac'
USER_EMAIL = 'sme@nju.edu.cn'
USER_PASSWD = '789456'
DB_HOSTNAME = 'localhost'
DB_PORT = '3306'
DB_USERNAME = 'szy'
DB_PASSWORD = '123456'
DB_NAME = 'weixin'
ADDRESS = '123.123.132.13'


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'xxxxx'

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True


class ProductionConfig(Config):
    pass


config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
