# -*- coding:utf8 -*-
# Author: shizhenyu96@gamil.com
# github: https://github.com/imndszy
from __future__ import absolute_import

from .wxconfig import WxApiUrl
from .wxapi import CommunicateWithApi
from .wxtemplate import send_common_template_msg


__author__ = 'shizhenyu'
__version__ = '1.0.0'
__all__ = ('WxApiUrl',
           'CommunicateWithApi',
           'send_common_template_msg')
