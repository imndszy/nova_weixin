# -*- coding:utf8 -*-
# Author: shizhenyu96@gamil.com
# github: https://github.com/imndszy
import time
# from msg_format import *
from app.lib.database import mysql
from app.nova.get_user_info import get_stuid,Student


person_info_key = ['daily_assess', 'gpa', 'recom', 'tutor']
mes_key = ['not_read_mes', 'history_mes', 'recent_mes']

def save_into_database(content,openid):
    stuid = get_stuid(openid)
    sql = "insert into queryrecord values('%s',%s,'%s','')" % (content,int(time.time()),stuid)

    @mysql(sql)
    def save(results=''):
        return results
    save()
    return 0

def handle_event(msg):
    if msg['Event'] == 'subscribe':
        if msg['EventKey']:
            stuid = msg['EventKey'][8:]
            openid = msg['FromUserName']
            sql = "update biding set openid = '%s' where stuid = %s" % (openid,stuid)

            @mysql(sql)
            def update_binding(results=''):
                return results
            update_binding()
            return 0
        return "感谢关注！"

    if msg['Event'] == 'CLICK':
        if msg['EventKey'] in person_info_key:
            stu = Student(msg['FromUserName'])

            if msg['EventKey'] == person_info_key[0]:  # 日常行为考核
                rout = stu.get_routine_appraise()
                if type(rout) == type({}):
                    content = '总分: ' + str(stu.routine) + '\n基础考核项: ' + str(stu.routine_base) + '\n鼓励参与项: ' \
                              + str(
                        stu.routine_encou) + '\n成果奖励项: ' + str(stu.routine_develop) + '\n排名:' + \
                              str(stu.routine_rank)
                else:
                    content = rout
                return content

            if msg['EventKey'] == person_info_key[1]:  # gpa查询
                gpa = stu.get_gpa()
                if type(gpa) == type({}):
                    your_gpa = str(stu.gpa)
                    your_gpa_rank = str(stu.gpa_rank)
                    rank_percent = str(round(float(stu.gpa_rank) / gpa['max'] * 100, 2)) + '%'
                    your_next_gpa = str(round(gpa['next'], 4))
                    your_prev_gpa = str(round(gpa['prev'], 4))
                    your_first_gpa = str(round(gpa['first'], 4))
                    content = 'GPA: ' + your_gpa + '\nRank: ' + your_gpa_rank + '\n您位于' + rank_percent + \
                              '\n前一名的绩点: ' + your_prev_gpa + '\n后一名的绩点: ' + your_next_gpa + '\n第一名的绩点: ' \
                              + your_first_gpa
                else:
                    content = gpa
                return content

            if msg['EventKey'] == person_info_key[2]:  # 推免查询
                gpa = stu.get_recom()
                if type(gpa) == type({}):
                    your_gpa = str(stu.gpa)
                    your_gpa_rank = str(stu.gpa_rank)
                    rank_percent = str(round(float(stu.gpa_rank) / gpa['max'] * 100, 2)) + '%'
                    your_next_gpa = str(round(gpa['next'], 4))
                    your_prev_gpa = str(round(gpa['prev'], 4))
                    your_first_gpa = str(round(gpa['first'], 4))
                    twenty_per_gpa = str(round(gpa['twenty_per'], 4))
                    content = '总GPA排名\n' + '*' * 22 + '\nGPA: ' + your_gpa + '\nRank: ' + your_gpa_rank + '\n您位于' \
                              + rank_percent + '\n前一名的绩点: ' + your_prev_gpa + '\n后一名的绩点: ' + your_next_gpa \
                              + '\n第一名的绩点: ' + your_first_gpa + '\n排名20%的GPA:' + twenty_per_gpa
                else:
                    content = gpa
                return content

            if msg['EventKey'] == person_info_key[3]:  # 导师查询
                tutor = stu.get_tutor()
                if type(tutor) == type({}):
                    if tutor['status']:
                        content = '您的导师是: ' + stu.tutor + '\nemail:' + stu.tutor_mail + '\n' + '=' * 18 + '\n'
                        if tutor['same_tutor']:
                            content = content + '导师与您相同的有:\n\n'
                            info_list = []
                            for i in tutor['same_tutor']:
                                info_list.append(i[1] + ' ' + i[2] + '\n宿舍: ' + i[4])
                            content = content + '\n\n'.join(info_list)
                        else:
                            content = content + '没有人和您有相同导师！'
                    else:
                        content = '您当前没有导师！'
                else:
                    content = tutor
                return content

        if msg['EventKey'] in mes_key:
            if msg['EventKey'] == 'not_read_mes':
                pass
        else:
            return '错误的菜单值！'
    else:
        return 'wrong_key'


class MsgHandler(object):
    def __init__(self, msg):
        self.type = msg.get('MsgType')
        self.to_user = msg.get('ToUserName')
        self.from_user = msg.get('FromUserName')
        self.create_time = msg.get('CreateTime')
        self.msgid = msg.get('MsgId', 'not_event')
        if self.type == 'text':
            self.content = msg.get('Content')
            save_into_database(self.content,self.from_user)
        elif self.type == 'image':
            self.picurl = msg.get('PicUrl')
            self.media_id = msg.get('MediaId')
            save_into_database(self.picurl, self.from_user)
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















