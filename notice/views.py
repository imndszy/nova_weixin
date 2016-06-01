# -*- coding:utf8 -*-
# Author: shizhenyu96@gamil.com
# github: https://github.com/imndszy
from flask import render_template, redirect, request, url_for, flash
from nova_weixin.config import root,passwd
from . import auth
from .forms import LoginForm

@auth.route('/login', methods = ['GET', 'POST'])
def login():
    user = None
    form = LoginForm()
    if form.validate_on_submit():
        user = form.username.data
        password = form.password.data
        if user == root and password == passwd:
            return redirect(request.args.get('next') or url_for('main.index'))
        flash("Invalid username or password!")
    return render_template('auth/login.html',form=form)

@auth.route('/article',methods = ['GET','POST'])
def article():
    pass
