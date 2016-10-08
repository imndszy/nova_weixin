# -*- coding:utf8 -*-
# Author: shizhenyu96@gamil.com
# github: https://github.com/imndszy
import os

from nova_weixin.app import create_app


app = create_app(os.getenv('FLASK_CONFIG') or 'default')


if __name__ == "__main__":
    app.run()
