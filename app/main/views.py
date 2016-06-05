from flask import render_template
from . import main


@main.route('/')
def index():
    return render_template('main/index.html')

@main.route('/wrong')
def wrong():
    return render_template('main/wrong.html')
