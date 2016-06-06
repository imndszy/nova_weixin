# -*- coding:utf8 -*-
# Author: shizhenyu96@gamil.com
# github: https://github.com/imndszy
import time
from flask import (render_template, redirect, request, url_for, flash, session)
from flask.ext.login import login_user, logout_user, login_required
from . import auth
from .. import db
from ..models import User
from .forms import LoginForm, RegistrationForm,ArticleForm
from get_users import classes,stu,create_class_html,create_stu_html
from noteprocess import note_index,note_content,note_response,send
from config import ROOT_USER


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            return redirect(request.args.get('next') or url_for('auth.article'))
        flash('Invalid username or password.')
    return render_template('auth/login.html', form=form)


@auth.route('/article',methods=['GET', 'POST'])
@login_required
def article():
    form = ArticleForm()
    if form.validate_on_submit():
        article_url = form.url.data
        image_url = form.image_url.data
        title = form.title.data
        session['article_url'] = article_url
        session['image_url'] = image_url
        session['title'] = title
        class_dict = classes()
        create_class_html(class_dict)
        return redirect(request.args.get('next') or url_for('auth.choose_class'))
    return render_template('auth/article.html', form=form)

@auth.route('/choose_class',methods=['GET', 'POST'])
@login_required
def choose_class():
    if request.method == 'POST':
        class_list = request.form.getlist('checked')
        class_dict = classes()
        if 'choose_all' in class_list:
            class_list = [i for i in class_dict.keys() if i not in class_list]
        session['classes'] = class_list
        stu_dict = stu(class_list)
        create_stu_html(stu_dict,class_dict)
        return redirect(url_for('auth.choose_stu'))
    return render_template('auth/class.html')

@auth.route('/choose_stu',methods=['GET', 'POST'])
@login_required
def choose_stu():
    if session['classes']:
        article_url = session['article_url'].encode('utf8')
        image_url = session['image_url'].encode('utf8')
        title = session['title'].encode('utf8')
        if request.method == 'POST':
            stu_list = request.form.getlist('checked')
            class_list = session['classes']
            chosen_class_stu= []
            for m in stu(class_list).values():
                for n in m:
                    chosen_class_stu.append(str(n[0]))
            if 'choose_stu_all' in stu_list:
                stu_list = [i for i in chosen_class_stu if i not in stu_list]
            nid = int(time.time())
            note_index(article_url,image_url,stu_list,nid)
            note_content(article_url,image_url,title,nid)
            note_response(nid)
            if send(title, article_url, stu_list) == -1:
                return render_template('auth/fail.html')
            session['finish'] = 'finished'
            return redirect(url_for('auth.finish'))
        return render_template('auth/stu.html')
    return redirect(url_for('auth.article'))

@auth.route('/finish',methods=['GET','POST'])
@login_required
def finish():
    if session['finish'] == 'finished':
        return render_template('auth/finish.html')
    return redirect(url_for('auth.article'))

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('main.index'))


@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        if form.username.data == ROOT_USER:
            user = User(email=form.email.data,
                        username=form.username.data,
                        password=form.password.data)
            db.session.add(user)
            flash('You can now login.')
            return redirect(url_for('auth.login'))
        else:
            flash('Must be Novaer!')
            return redirect(url_for('main.wrong'))
    return render_template('auth/register.html', form=form)
