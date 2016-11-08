# -*- coding:utf8 -*-
# Author: shizhenyu96@gamil.com
# github: https://github.com/imndszy
"""

以下用到encode的地方均是因为从数据库取出的数据为utf8，否则会出现UnicodeError

"""
import time
from flask import make_response
from msg_format import *
from nova_weixin.app.lib.database import mysql
from nova_weixin.app.nova.get_user_info import get_stuid, Student


person_info_key = ['daily_assess', 'gpa', 'recom', 'tutor']
mes_key = ['not_read_mes', 'history_mes']


def save_into_database(content, openid):
    stuid = get_stuid(openid)
    sql = "insert into queryrecord "\
          "values('%s',%s,'%s','')" % (content, int(time.time()), stuid)

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
            sql = "update biding set openid = '%s' "\
                  "where stuid = %d" % (openid, stuid)

            @mysql(sql)
            def update_binding(results=''):
                return results
            update_binding()
            return "您已成功关注工程管理！"
        return "感谢关注！"

    if msg['Event'] == 'unsubscribe':
        return ""

    if msg['Event'] == 'CLICK':
        if msg['EventKey'] in mes_key:
            return handle_mes_key(msg)
        if msg['EventKey'] in person_info_key:
            stu = Student(msg['FromUserName'])

            if msg['EventKey'] == person_info_key[0]:  # 日常行为考核
                rout = stu.get_routine_appraise()
                if isinstance(rout, dict):
                    content = '总分: ' + str(stu.routine) + '\n基础考核项: ' \
                              + str(stu.routine_base) + '\n鼓励参与项: ' \
                              + str(stu.routine_encou) + '\n成果奖励项: ' \
                              + str(stu.routine_develop) + '\n排名:' + \
                              str(stu.routine_rank)
                else:
                    content = rout
                return content

            if msg['EventKey'] == person_info_key[1]:  # gpa查询
                gpa = stu.get_gpa()
                if isinstance(gpa, dict):
                    your_gpa = str(stu.gpa)
                    your_gpa_rank = str(stu.gpa_rank)
                    rank_percent = str(round(float(stu.gpa_rank) / gpa['max'] * 100, 2)) + '%'
                    your_next_gpa = str(round(gpa['next'], 4))
                    your_prev_gpa = str(round(gpa['prev'], 4))
                    your_first_gpa = str(round(gpa['first'], 4))
                    content = 'GPA: ' + your_gpa + '\nRank: ' + your_gpa_rank \
                              + '\n您位于' + rank_percent + \
                              '\n前一名的绩点: ' + your_prev_gpa + '\n后一名的绩点: ' \
                              + your_next_gpa + '\n第一名的绩点: ' \
                              + your_first_gpa
                else:
                    content = gpa
                return content

            if msg['EventKey'] == person_info_key[2]:  # 推免查询
                gpa = stu.get_recom()
                if isinstance(gpa, dict):
                    your_gpa = str(stu.gpa)
                    your_gpa_rank = str(stu.gpa_rank)
                    rank_percent = str(round(float(stu.gpa_rank) / gpa['max'] * 100, 2)) + '%'
                    your_next_gpa = str(round(gpa['next'], 4))
                    your_prev_gpa = str(round(gpa['prev'], 4))
                    your_first_gpa = str(round(gpa['first'], 4))
                    twenty_per_gpa = str(round(gpa['twenty_per'], 4))
                    content = '总GPA排名\n' + '*' * 22 + '\nGPA: ' + your_gpa \
                              + '\nRank: ' + your_gpa_rank + '\n您位于' \
                              + rank_percent + '\n前一名的绩点: ' + your_prev_gpa \
                              + '\n后一名的绩点: ' + your_next_gpa \
                              + '\n第一名的绩点: ' + your_first_gpa + '\n排名20%的GPA:' + twenty_per_gpa
                else:
                    content = gpa
                return content

            if msg['EventKey'] == person_info_key[3]:  # 导师查询
                tutor = stu.get_tutor()
                if isinstance(tutor, dict):
                    if tutor['status']:
                        content = '您的导师是: ' + stu.tutor.encode('utf8') \
                                  + '\nemail:' + stu.tutor_mail.encode('utf8') \
                                  + '\n' + '=' * 18 + '\n'
                        if tutor['same_tutor']:
                            content = content + '导师与您相同的有:\n\n'
                            info_list = []
                            for i in tutor['same_tutor']:
                                info_list.append(i[1].encode('utf8') + ' ' +
                                                 i[2].encode('utf8') +
                                                 '\n宿舍: ' +
                                                 i[4].encode('utf8'))
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


def handle_mes_key(msg):
    stuid = get_stuid(msg['FromUserName'])
    sql = 'select nid,readlist from noteresponse'

    @mysql(sql)
    def sel(results=''):
        return results
    re = sel()
    read = [i[0] for i in re if str(stuid) in i[1]]

    sql = 'select nid,stuids from noteindex'

    @mysql(sql)
    def sel2(results=''):
        return results

    re2 = sel2()

    send = [j[0] for j in re2 if str(stuid) in j[1]]

    not_read = list(set(send)-set(read))

    sql = 'select nid,title,picurl,url from notecontent'
    @mysql(sql)
    def sel3(results=''):
        return results
    content = sel3()
    content = [(x[1],'',x[2],x[3]) for x in content if x[0] in not_read]
    content.reverse()
    send_content =content[:10]
    middle_str=''
    for i in send_content:
        middle_str += news_rep_middle % i

    head_str = news_rep_front % (msg['FromUserName'], msg['ToUserName'], str(int(time.time())),len(send_content))
    content = head_str+middle_str+news_rep_back
    response = make_response(content)
    response.content_type = 'application/xml'
    return response



