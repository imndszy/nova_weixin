# -*- coding:utf8 -*-
# Author: shizhenyu96@gamil.com
# github: https://github.com/imndszy
"""

以下用到encode的地方均是因为从数据库取出的数据为utf8，否则会出现UnicodeError

"""
import time
from msg_format import *
# from nova_weixin.app.lib.database import mysql
from nova_weixin.app.nova.get_user_info import get_stuid, Student
from nova_weixin.app.config import ADDRESS
from nova_weixin.app.weixin.weixinconfig import APP_ID
from nova_weixin.packages.novamysql import insert, update, select

person_info_key = ['daily_assess', 'gpa', 'recom', 'tutor']
mes_key = ['not_read_mes', 'history_mes']


def save_into_database(content, openid):
    stuid = get_stuid(openid)
    result = insert('queryrecord', keyword=content, time=int(time.time()), username=stuid, describe='')
    # sql = "insert into queryrecord "\
    #       "values('%s',%d,'%s','')" % (content, int(time.time()), stuid)
    #
    # @mysql(sql)
    # def save(results=''):
    #     return results
    # save()
    # return 0
    if result == 1:
        return 0
    else:
        return -1


def handle_event(msg):
    if msg['Event'] == 'subscribe':
        if msg['EventKey']:
            stuid = msg['EventKey'][8:]
            openid = msg['FromUserName']
            result = update('update biding set openid = ? where stuid = ?', openid, stuid)
            # sql = "update biding set openid = '%s' "\
            #       "where stuid = %s" % (openid, stuid)
            #
            # @mysql(sql)
            # def update_binding(results=None):
            #     return results
            # update_binding()
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


def handle_mes_key(msg):
    stuid = get_stuid(msg['FromUserName'])

    send_info = select('select nid,stuids from noteindex')

    if not send_info:
        return ''

    send = [j['nid'] for j in send_info if str(stuid) in j['stuids']]

    if not send:
        return ''

    read_info = select('select nid,readlist from noteresponse')

    if not read_info:
        return ''

    read = [i['nid'] for i in read_info if str(stuid) in i['readlist']]
    # sql = 'select nid,readlist from noteresponse'
    #
    # @mysql(sql)
    # def sel(results=None):
    #     return results
    # re = sel()
    # if not re:
    #     return ''
    # if isinstance(re[0],tuple):
    #     read = [i[0] for i in re if str(stuid) in i[1]]
    #     print read
    # else:
    #     if str(stuid) not in re[1]:
    #         read = []
    #     else:
    #         read = re[:1]
    #
    # sql = 'select nid,stuids from noteindex'
    #
    # @mysql(sql)
    # def sel2(results=None):
    #     return results
    #
    # re2 = sel2()
    # if not re2:
    #     return ''
    # if isinstance(re2[0],tuple):
    #     send = [j[0] for j in re2 if str(stuid) in j[1]]
    # else:
    #     if str(stuid) not in re2[1]:
    #         send = []
    #     else:
    #         send = re2[:1]

    not_read = list(set(send)-set(read))

    if not not_read:
        return ''

    send_content = select('select nid,title,picurl,url from notecontent order by nid desc')
    #
    # sql = 'select nid,title,picurl,url from notecontent order by nid desc'
    # @mysql(sql)
    # def sel3(results=None):
    #     return results
    #
    # content = sel3()
    # if isinstance(content[0],tuple):
    #     # content.reverse()
    #     send_content = content[:10]
    # else:
    #     send_content = [tuple(content)]
    def transfer_url(nid):
        url = ADDRESS + '/code/' + str(nid)
        post_url = 'https://open.weixin.qq.com/connect/oauth2/authorize?' \
                   'appid=%s&redirect_uri=%s' \
                   '&response_type=code&scope=snsapi_base&state=123' \
                   '#wechat_redirect' % (APP_ID, url)
        return post_url

    send_content = [(x['title'],'',x['picurl'],transfer_url(x['url'])) for x in send_content if x['nid'] in not_read]

    middle_str=''
    for i in send_content:
        middle_str += news_rep_middle % i

    head_str = news_rep_front % (msg['FromUserName'], msg['ToUserName'], str(int(time.time())),len(send_content))
    content = head_str+middle_str+news_rep_back
    return content
