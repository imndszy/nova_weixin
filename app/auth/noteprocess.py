# -*- coding:utf8 -*-
# Author: shizhenyu96@gamil.com
# github: https://github.com/imndszy
from nova_weixin.packages.novalog import NovaLog
from nova_weixin.packages.novamysql import insert


log = NovaLog(path='log/db_operation.log')
send_log = NovaLog(path='log/runtime.log')

def note_index(stu_list, nid):
    stu_text = ''
    for i in stu_list:
        stu_text = stu_text + str(i)
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
