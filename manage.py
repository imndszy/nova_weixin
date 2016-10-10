# -*- coding:utf8 -*-
# Author: shizhenyu96@gamil.com
# github: https://github.com/imndszy
import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import nova_weixin.app


app = nova_weixin.app.create_app(os.getenv('FLASK_CONFIG') or 'production')


if __name__ == "__main__":
    app.run()
