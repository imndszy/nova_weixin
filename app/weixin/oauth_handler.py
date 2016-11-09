# -*- coding:utf8 -*-
# Author: shizhenyu96@gamil.com
# github: https://github.com/imndszy
import json
import urllib2
import time
import logging

from nova_weixin.app.weixin.weixinconfig import APP_ID, SECRET
from nova_weixin.app.nova.get_user_info import get_stuid
from nova_weixin.app.lib.database import mysql


def get_openid_from_code(code):
    """
    fetch user's openid with code from oauth
    :param code: 向用户发起网页授权后用户同意后获取到的code，scope参数为snsapi_base，
                  详见微信公众平台开发者文档（http://mp.weixin.qq.com/wiki/17/c0f37d5704f0b64713d5d2c37b468d75.html）
    :return:正确返回的json:
               {
               "access_token":"ACCESS_TOKEN",
               "expires_in":7200,
               "refresh_token":"REFRESH_TOKEN",
               "openid":"OPENID",
               "scope":"SCOPE",
               "unionid": "..."
               }
               有错误时返回的json:{"errcode":40029,"errmsg":"invalid code"}
    """
    url = "https://api.weixin.qq.com/sns/oauth2/access_token?" \
          "appid=%s&secret=%s&code=%s"\
          "&grant_type=authorization_code" % (APP_ID, SECRET, code)
    result = urllib2.urlopen(url).read()
    return json.loads(result)['openid']


def jiaowu(openid):
    stuid = get_stuid(openid)
    if not stuid:
        return -1
    sql = "select email,status from stuinfo where stuid=%s" % stuid

    @mysql(sql)
    def get_jiaowu(results=None):
        return results
    result = get_jiaowu()
    if result:
        result.append(stuid)
        return result
    else:
        return 0

def jiaowu_save(stuid,email,status):
    sql = "update stuinfo set email = '%s',status = %d where stuid = %d" % (email,status,stuid)

    @mysql(sql)
    def save(results=None):
        return results
    save()

def openid_handler(openid, post_url):
    """
    update the mysql database using openid and post_url
    :param openid: openid of the user who read the specific article
    :param post_url: the url of the article
    :return: return the result of the mysql's update
    """
    stuid = get_stuid(openid)
    read = int(time.time())
    sql = "select nID from notecontent where url = '" + post_url + "'"

    @mysql(sql)
    def get_url(results=None):
        if len(results)>1:
            nid = results[0][0]
        elif len(results) == 1:
            nid = results[0]
        else:
            nid = -1
        return nid
    nid = get_url()

    sql2 = "select * from noteresponse where nID = %d" % nid

    @mysql(sql2)
    def get_read_info(results=None):
        if results:
            return results
        else:
            logging.basicConfig(level=logging.DEBUG,
                                format='%(asctime)s %(filename)s[line:%(lineno)d]'
                                       '%(levelname)s %(message)s',
                                datefmt='%a, %d %b %Y %H:%M:%S',
                                filename='./log/database.log',
                                filemode='w')
            pass
    results = get_read_info()
    earliest = results[1]
    read_id = results[3].split(",")[:-1]  # "a list"
    read_time = results[4].split(",")[:-1]  # "a list"
    read_pop = results[5]
    if earliest == 0:
        earliest = read
    latest = read
    if stuid not in read_id:
        read_id.append(str(stuid))
        read_id = ','.join(read_id) + ','   #a string
        read_pop = read_pop + 1

    read_time.append(str(stuid) + ':' + str(read))   #a list
    read_time = ','.join(read_time) + ','   #a string
    sql_all = "update noteresponse set readList='" + read_id + "'," + "readTime = '" + read_time + "',"\
              + "earlistRead = %d,latestRead = %d,readPop =%d where nID = %d;" % (earliest,latest,read_pop,nid)

    @mysql(sql_all)
    def update(results=None):
        #log here
        return results
    update()

#
# def history_latest():
#     sql = "select nid from noteindex order by nid desc limit 1"
#
#     @mysql(sql)
#     def get(results=''):
#         return results
#     latest = get()
#     return latest[0]


def history_articles(stuid):
    sql = "select nid,stuids from noteindex"

    @mysql(sql)
    def get(results=None):
        return results

    result = get()
    nids = []
    for i in result:
        if str(stuid) in i[1]:
            nids.append(i[0])
    articles = []
    article_dict = dict()
    article_dict['articles'] = dict()
    for x in nids:
        sql = "select nid,title,url from notecontent where nid = %d" % x

        @mysql(sql)
        def get_content(results=None):
            return results

        re = get_content()
        articles.append(re)
    return articles