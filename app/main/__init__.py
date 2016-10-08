# -*- coding:utf8 -*-
# Author: shizhenyu96@gamil.com
# github: https://github.com/imndszy
from flask import Blueprint
main = Blueprint('main', __name__)
from nova_weixin.app.main import views, errors
