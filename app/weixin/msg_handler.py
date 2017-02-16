# -*- coding:utf8 -*-
# Author: shizhenyu96@gamil.com
# github: https://github.com/imndszy
"""

以下用到encode的地方均是因为从数据库取出的数据为utf8，否则会出现UnicodeError

"""
import time
from flask import make_response
from nova_weixin.app.weixin.msg_format import *
from nova_weixin.app.nova.get_user_info import get_stuid, Student
from nova_weixin.app.config import ADDRESS
from nova_weixin.app.weixin.weixinconfig import APP_ID
from nova_weixin.packages.novamysql import insert, update, select
from nova_weixin.packages.nova_wxsdk import WxApiUrl
from nova_weixin.packages.novalog import NovaLog

person_info_key = ['daily_assess', 'gpa', 'recom', 'tutor']
mes_key = ['not_read_mes', 'history_mes']

log = NovaLog('log/db_operation.log')

def __save_into_database(content, openid):
    stuid = get_stuid(openid)
    result = insert('queryrecord', keyword=content, time=int(time.time()), username=stuid, describe='')

    if result == 1:
        return 0
    else:
        return -1


def handle_msg(msg):
    if msg['MsgType'] == 'text':
        try:
            __save_into_database(msg['Content'], msg['FromUser'])
        except:
            pass
        finally:
            return ""

    if msg['MsgType'] == 'event':
        if msg['Event'] == 'CLICK' and msg['EventKey'] == 'not_read_mes':
            return __handle_mes_key(msg)
        return __res_text_msg(msg, __handle_event(msg))


def __handle_event(msg):
    if msg['Event'] == 'subscribe':
        if msg['EventKey']:
            stuid = msg['EventKey'][8:]
            openid = msg['FromUserName']
            result = update('update biding set openid = ? where stuid = ?', openid, stuid)

            if result != 1:
                log.critical("unable bide openid={openid} and stuid={stuid}".format(openid=openid, stuid=stuid))
            return "您已成功关注工程管理！"
        return "感谢关注！"

    if msg['Event'] == 'SCAN':
        return "您已成功再次关注…然而并没有什么用～"

    if msg['Event'] == 'unsubscribe':
        return ""

    if msg['Event'] == 'CLICK' and msg['EventKey'] in person_info_key:
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
                if gpa.get('nonnext'):
                    your_next_gpa = gpa['next']
                else:
                    your_next_gpa = str(round(gpa['next'], 4))

                if gpa.get('nonprev'):
                    your_prev_gpa = gpa['prev']
                else:
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
                if gpa.get('nonnext'):
                    your_next_gpa = gpa['next']
                else:
                    your_next_gpa = str(round(gpa['next'], 4))

                if gpa.get('nonprev'):
                    your_prev_gpa = gpa['prev']
                else:
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
                            info_list.append(i['name'].encode('utf8') + ' ' +
                                             i['sex'].encode('utf8') +
                                             '\n宿舍: ' +
                                             i['campus'].encode('utf8'))
                        content = content + '\n\n'.join(info_list)
                    else:
                        content = content + '没有人和您有相同导师！'
                else:
                    content = '您当前没有导师！'
            else:
                content = tutor
            return content


def __handle_mes_key(msg): # 未读消息处理
    stuid = get_stuid(msg['FromUserName'])

    send_info = select('select nid,stuids from noteindex')
    if not send_info:
        return ''

    # 发送给某学生的所有消息
    send = [j['nid'] for j in send_info if str(stuid) in j['stuids']]
    if not send:
        return ''

    read_info = select('select nid,readlist from noteresponse')
    if not read_info:
        return ''

    # 该学生已读的所有消息
    read = [i['nid'] for i in read_info if str(stuid) in i['readlist']]

    not_read = list(set(send)-set(read))
    if not not_read:
        return ''

    send_content = select('select nid,title,picurl,url from notecontent order by nid desc')

    def transfer_url(nid):
        url = ADDRESS + '/code/' + str(nid)
        post_url = WxApiUrl.oauth2_new_page.format(appid=APP_ID, redirect_url=url)
        return post_url

    send_content = [(x['title'],'',x['picurl'],transfer_url(x['url'])) for x in send_content if x['nid'] in not_read]

    middle_str=''
    for i in send_content:
        middle_str += news_rep_middle % i

    head_str = news_rep_front % (msg['FromUserName'], msg['ToUserName'], str(int(time.time())),len(send_content))
    content = head_str+middle_str+news_rep_back
    return __res_news_msg(content)


def __res_news_msg(content):
    response = make_response(content)
    response.content_type = 'application/xml'
    return response


def __res_text_msg(msg, content):
    response = make_response(text_rep % (msg['FromUserName'], msg['ToUserName'], str(int(time.time())), content))
    response.content_type = 'application/xml'
    return response
