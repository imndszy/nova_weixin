# -*- coding:utf8 -*- 
# Author: shizhenyu96@gamil.com
# github: https://github.com/imndszy
from flask import Blueprint
weixin = Blueprint('weixin',__name__)
from nova_weixin.app.weixin import main