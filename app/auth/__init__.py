# -*- coding:utf8 -*-
# Author: shizhenyu96@gamil.com
# github: https://github.com/imndszy
# 注册在该蓝图下的路由由管理员使用

from flask import Blueprint
auth = Blueprint('auth', __name__)
from nova_weixin.app.auth import views
