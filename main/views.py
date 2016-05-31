# -*- coding:utf8 -*-
# Author: shizhenyu96@gamil.com
# github: https://github.com/imndszy
from flask import render_template
from . import main

@main.route('/')
def index():
    return render_template('index.html')