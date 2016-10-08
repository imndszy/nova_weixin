from flask import Flask
from flask.ext.bootstrap import Bootstrap
from flask.ext.moment import Moment
from config import config

bootstrap = Bootstrap()
moment = Moment()


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    bootstrap.init_app(app)
    moment.init_app(app)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint,url_prefix='/main')

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')

    from .weixin import weixin as weixin_blueprint
    app.register_blueprint(weixin_blueprint)

    from .bind import bind as bind_blueprint
    app.register_blueprint(bind_blueprint, url_prefix='/bind')

    return app