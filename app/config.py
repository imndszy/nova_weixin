# -*- coding:utf8 -*- 
# Author: shizhenyu96@gamil.com
# github: https://github.com/imndszy
import os
import sys
basedir = os.path.abspath(os.path.dirname(__file__))

ROOT_USER = 'nova_cac'               # 后台管理员用户名
USER_EMAIL = 'sme@nju.edu.cn'        # 后台管理员邮箱
USER_PASSWD = 'test'                 # 后台管理员密码
DB_HOSTNAME = 'localhost'            # 数据库地址
DB_PORT = 3306             
DB_USERNAME = 'szy'
DB_PASSWORD = '123456'
DB_NAME = 'weixin' 
ADDRESS = 'http://121.42.216.141'    # 主机地址
PY2 = sys.version_info[0] == 2


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hqgg09-9(G_)dert-jg'

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
