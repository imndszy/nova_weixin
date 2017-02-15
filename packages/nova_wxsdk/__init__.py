# -*- coding:utf8 -*-
# Author: shizhenyu96@gamil.com
# github: https://github.com/imndszy
from __future__ import absolute_import

from .wxurl import WxApiUrl
from .wxapi import CommunicateWithApi
from .wxtemplate import send_common_template_msg
from .wxacctoken import get_token
from .wxqrcode import create_ticket,get_qrcode_url


__author__ = 'shizhenyu'
__version__ = '1.0.0'
__all__ = ('WxApiUrl',
           'CommunicateWithApi',
           'send_common_template_msg',
           'get_token',
           'create_ticket',
           'get_qrcode_url')
