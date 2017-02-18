# -*- coding:utf8 -*-
# Author: shizhenyu96@gamil.com
# github: https://github.com/imndszy
import os

from flask import Flask
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from .config import (config, DB_HOSTNAME, DB_PASSWORD,
                     DB_USERNAME, DB_NAME, DB_PORT)
from nova_weixin.packages.novamysql import create_engine

bootstrap = Bootstrap()
moment = Moment()


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    os.environ['config_flask'] = config_name

    if not os.path.exists('./log'):
        os.mkdir('./log')
    create_engine(DB_USERNAME, DB_PASSWORD, DB_NAME, DB_HOSTNAME, DB_PORT)
    bootstrap.init_app(app)
    moment.init_app(app)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint, url_prefix='/main')

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')

    from .weixin import weixin as weixin_blueprint
    app.register_blueprint(weixin_blueprint)

    from .bind import bind as bind_blueprint
    app.register_blueprint(bind_blueprint, url_prefix='/bind')

    return app
