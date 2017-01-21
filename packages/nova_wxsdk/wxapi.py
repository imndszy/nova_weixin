# -*- coding:utf8 -*-
# Author: shizhenyu96@gamil.com
# github: https://github.com/imndszy
import requests


class CommunicateWithApi(object):

    @staticmethod
    def get_data(url):
        return requests.get(url).json()

    @staticmethod
    def post_data(url, data=None):
        return requests.post(url, data=data).json()