# -*- coding:utf8 -*-
# Author: shizhenyu96@gamil.com
# github: https://github.com/imndszy
from flask import Blueprint
bind = Blueprint('bind', __name__)
from nova_weixin.app.bind import views