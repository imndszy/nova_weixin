from flask import render_template, redirect, request, url_for, flash, session
from flask.ext.login import login_user, logout_user, login_required, \
    current_user
from . import auth
from .. import db
from ..models import User
from .forms import LoginForm, RegistrationForm,ArticleForm


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
        session['article_url'] = article_url
        session['image_url'] = image_url
        return redirect(request.args.get('next') or url_for('auth.touser'))
    return render_template('auth/article.html', form=form)

@auth.route('/touser',methods=['GET', 'POST'])
@login_required
def touser():
    article_url = session['article_url']
    image_url = session['image_url']
    if request.method == 'POST':
        pass
    return render_template('index.html')

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
        user = User(email=form.email.data,
                    username=form.username.data,
                    password=form.password.data)
        db.session.add(user)
        flash('You can now login.')
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html', form=form)
