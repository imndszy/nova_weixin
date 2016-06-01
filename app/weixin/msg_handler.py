# -*- coding:utf8 -*-
# Author: shizhenyu96@gamil.com
# github: https://github.com/imndszy
import time
from msg_format import *


class MsgHandler(object):
    def __init__(self, msg):
        self.type = msg.get('MsgType')
        self.to_user = msg.get('ToUserName')
        self.from_user = msg.get('FromUserName')
        self.create_time = msg.get('CreateTime')
        self.msgid = msg.get('MsgId', 'not_event')
        if self.type == 'text':
            self.content = msg.get('Content')
        elif self.type == 'image':
            self.picurl = msg.get('PicUrl')
            self.media_id = msg.get('MediaId')
        elif self.type == 'voice':
            self.voice_format = msg.get('Format')
            self.media_id = msg.get('MediaId')
        elif self.type == 'video' or self.type == 'shortvideo':
            self.thumb_media_id = msg.get('ThumbMediaId')
            self.media_id = msg.get('MediaId')
        elif self.type == 'location':
            self.location_x = msg.get('Location_X')
            self.location_y = msg.get('Location_Y')
            self.scale = msg.get('Scale')
            self.label = msg.get('Label')
        elif self.type == 'link':
            self.title = msg.get('Title')
            self.description = msg.get('Description')
            self.url = msg.get('Url')
        elif self.type == 'event':
            self.event = msg.get('Event')
            if self.event == 'subscribe':
                self.event_key = msg.get('EventKey')
                pass
            elif self.event == 'SCAN':
                self.ticket = msg.get('Ticket')
                self.event_key = msg.get('EventKey')
            elif self.event == 'LOCATION':
                self.latitude = msg.get('Latitude')
                self.longitude = msg.get('Longitude')
                self.precision = msg.get('Precision')
            elif self.event == 'CLICK':
                self.event_key = msg.get('EventKey')
                pass
            elif self.event == 'VIEW':
                self.event_key = msg.get('EventKey')
                pass

    def text(self):
        pass

    def image(self):
        pass

    def voice(self):
        pass

    def video(self):
        pass

    def location(self):
        pass

    def link(self):
        pass

    def event(self):
        pass















