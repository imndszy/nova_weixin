# -*- coding:utf8 -*-
# Author: shizhenyu96@gamil.com
# github: https://github.com/imndszy
import time
from nova_weixin.packages.novalog import NovaLog
from nova_weixin.packages.novamysql import insert, select_one, select, select_int
from nova_weixin.app.nova.get_user_info import get_stu_name


log = NovaLog(path='log/db_operation.log')
send_log = NovaLog(path='log/runtime.log')

def note_index(stu_list, nid):
    stu_text = ''
    for i in stu_list:
        stu_text = stu_text + str(i) + ','
    result = insert('noteindex', nid=nid, publishTime=nid, sort=0, topic='', stuids=stu_text, expire=0)

    if result == 1:
        return 0
    else:
        log.warn("insert into database error -- note_index")
        return -1


def note_content(arti_url, image_url, title, nid):
    result = insert('notecontent', nid=nid, title=title, publisher='cac', detail='', picurl=image_url, url=arti_url, tid=0)

    if result == 1:
        return 0
    else:
        log.warn("insert into database error -- note_content")
        return -1


def note_response(nid):
    result = insert('noteresponse',nid=nid, earlistread=0, latestread=0, readlist='', readtime='', readpop=0)

    if result == 1:
        return 0
    else:
        log.warn("insert into database error -- note_response")
        return -1


def get_read_info(nid, simple=False):
    send_stus = select_one('select stuids from noteindex where nid=?', nid)
    if not send_stus:
        return None
    if(',' in send_stus['stuids']):
        stu_send_list = send_stus['stuids'].split(',')[:-1]
    else:
        stu_send_list = [send_stus['stuids']]
    stu_send_list = list(set(stu_send_list))
    if simple:
        read_number = select_int('select readpop from noteresponse where nid=?', nid)
        if read_number is None:
            read_number=0
        return {'read_list': read_number, 'unread_list': len(stu_send_list)-read_number}

    read_info = select_one('select readTime from noteresponse where nid=?', nid)
    if not read_info:
        return None

    stu_read_list = [i.split(':')[0] for i in read_info['readtime'].split(',')[:-1]]
    stu_read_dicts_with_time = [{'stuid': i.split(":")[0],
                                 'time': __transfer_time(i.split(':')[1]),
                                 'name': get_stu_name(i.split(":")[0])} for i in read_info['readtime'].split(',')[:-1]]

    unread_stu = []
    for i in stu_send_list:
        if i in stu_read_list:
            pass
        else:
            unread_stu.append({'stuid':i, 'name':get_stu_name(i)})
    return {'read_list': stu_read_dicts_with_time, 'unread_list': unread_stu}


def get_activity_info():
    activities = select('select nid,title,url from notecontent order by nid desc limit 30')
    for i in activities:
        i['time'] = __transfer_time(i['nid'])
        read_info = get_read_info(i['nid'], simple=True)
        if read_info:
            i['read'] = read_info['read_list']
            i['unread'] = read_info['unread_list']
    return activities


def __transfer_time(timeStamp):
    try:
        timeArray = time.localtime(float(timeStamp))
    except ValueError as e:
        timeArray = time.localtime(1400000000.0)
    otherStyleTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
    return otherStyleTime
