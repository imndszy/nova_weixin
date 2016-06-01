# -*- coding:utf8 -*- 
# Author: shizhenyu96@gamil.com
# github: https://github.com/imndszy
import os
basedir = os.path.abspath(os.path.dirname(__file__))

# APP_ID = 'wx925d02f38'
# SECRET = 'aed361bef88'
# TOKEN = ''
# TEMPLATE_ID = ''
# MENU = {
#     "button": [
#         {
#
#             "name": "通知消息",
#             "sub_button": [
#                 {
#                     "type": "click",
#                     "name": "未读消息",
#                     "key": "not_read_mes"
#                 },
#                 {
#                     "type": "click",
#                     "name": "历史消息",
#                     "key": "history_mes"
#                 },
#                 {
#                     "type": "click",
#                     "name": "近期消息",
#                     "key": "recent_mes"
#                 }]
#
#         },
#         {
#             "name": "个人查询",
#             "sub_button": [
#                 {
#                     "type": "click",
#                     "name": "日常考核",
#                     "key": "daily_assess"
#                 },
#                 {
#                     "type": "click",
#                     "name": "绩点查询",
#                     "key": "gpa"
#                 },
#                 {
#                     "type": "click",
#                     "name": "推免查询",
#                     "key": "recom"
#                 },
#                 {
#                     "type": "click",
#                     "name": "导师查询",
#                     "key": "tutor"
#                 }
#             ]
#         },
#         {
#             "name": "个性服务",
#             "sub_button": [
#                 {
#                     "type": "view",
#                     "name": "微信问问",
#                     "url": ""
#                 },
#                 {
#                     "type": "view",
#                     "name": "教务推送",
#                     "url": ""
#                 },
#             ]
#
#         }
#
#     ]
# }
#
# root = 'aaa'
# root_id = 111
# passwd = 'bbb'
# CSRF_ENABLED = True
#
DB_HOSTNAME = 'localhost'
DB_PORT = '3306'
DB_USERNAME = 'root'
DB_PASSWORD = 'root'
DB_NAME = 'weixin'

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'xxxxx'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
                              'sqlite:///' + os.path.join(basedir, 'data-dev.sqlite')


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'data.sqlite')

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
