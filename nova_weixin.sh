#!/bin/bash
# Only works on Ubuntu
# mysql: {user: , password: }
apt-get update && apt-get -y upgrade
apt-get install -y git
apt-get install -y nginx
apt-get install -y supervisor
apt-get install -y python-dev python-setuptools
apt-get install -y python-pip
apt-get install -y python-virtualenv
apt-get install -y mysql-server mysql-client
cd /home && mkdir www && cd www && mkdir wechat && cd wechat
virtualenv env
git clone https://github.com/imndszy/nova_weixin.git
source env/bin/activate
pip install -r nova_weixin/requirements.txt
pip install uwsgi
deactivate
# 至此，基本软件的安装已经完成，接下来需进行相关软件的配置，包括uwsgi, supervisor, nginx，详见 http://blog.csdn.net/imjtrszy/article/details/53306260
# mysql需要新增用户进行权限管理，参见 http://blog.csdn.net/imjtrszy/article/details/53190300
# 以上事情都做完后修改微信相关的配置，主要包括 nova_weixin/app/config.py， nova_weixin/app/weixin/weixinconfig.py，前者包括系统相关配置，后者包括微信相关配置
