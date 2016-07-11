# -*- coding:utf8 -*-
# Author: shizhenyu96@gamil.com
# github: https://github.com/imndszy
from flask.ext.wtf import Form
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Regexp, EqualTo,URL
from wtforms import ValidationError


class BindForm(Form):
    stuid = StringField('Student ID', validators=[DataRequired()])
    certification = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Log In')