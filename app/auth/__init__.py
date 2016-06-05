# -*- coding:utf8 -*-
# Author: shizhenyu96@gamil.com
# github: https://github.com/imndszy
from flask import Blueprint
auth = Blueprint('auth', __name__)
from . import views
