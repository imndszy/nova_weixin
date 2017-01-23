# -*- coding:utf8 -*-
# Author: shizhenyu96@gamil.com
# github: https://github.com/imndszy
# import requests
import time

from nova_weixin.app.weixin.weixinconfig import APP_ID, SECRET
from nova_weixin.app.nova.get_user_info import get_stuid
# from nova_weixin.app.lib.database import mysql
from nova_weixin.packages.novamysql import select_one, update, select_int, select
from nova_weixin.packages.nova_wxsdk import WxApiUrl, CommunicateWithApi


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
    url = WxApiUrl.oauth2_token.format(appid=APP_ID, appsecret=SECRET, code=code)
    # url = "https://api.weixin.qq.com/sns/oauth2/access_token?" \
    #       "appid=%s&secret=%s&code=%s"\
    #       "&grant_type=authorization_code" % (APP_ID, SECRET, code)
    # result = requests.get(url).json()
    result = CommunicateWithApi.get_data(url)
    return result['openid']


def get_url(nid):
    return select_int('select url from notecontent where nid=?',nid)


def jiaowu(openid):
    stuid = get_stuid(openid)
    if not stuid:
        return -1
    info = select_one('select email,status from stuinfo where stuid=?', stuid)
    # sql = "select email,status from stuinfo where stuid=%s" % stuid
    #
    # @mysql(sql)
    # def get_jiaowu(results=None):
    #     return results
    # result = get_jiaowu()
    # if result:
    #     result.append(stuid)
    #     return result
    # else:
    #     return 0
    if info:
        info['stuid'] = stuid
        return info
    else:
        return -1

def jiaowu_save(stuid,email,status):
    result = update('update stuinfo set email = ?, status = ? where stuid = ?', email, status, stuid)
    # sql = "update stuinfo set email = '%s',status = %d where stuid = %d" % (email,status,stuid)
    #
    # @mysql(sql)
    # def save(results=None):
    #     return results
    # save()
    if result == 1:
        return 1
    else:
        return -1

def openid_handler(openid, nid):
    """
    update the mysql database using openid and post_url
    :param openid: openid of the user who read the specific article
    :param nid: the number of the article
    :return: return the result of the mysql's update
    """
    stuid = get_stuid(openid)
    read = int(time.time())
    # sql = "select nID from notecontent where url = '" + post_url + "'"
    #
    # @mysql(sql)
    # def get_url(results=None):
    #     if len(results)>1:
    #         nid = results[0][0]
    #     elif len(results) == 1:
    #         nid = results[0]
    #     else:
    #         nid = -1
    #     return nid
    # nid = get_url()

    # sql2 = "select * from noteresponse where nID = %d" % nid
    #
    # @mysql(sql2)
    # def get_read_info(results=None):
    #     if results:
    #         return results
    #
    # results = get_read_info()

    read_info = select_one('select * from noteresponse where nID =?', nid)
    earliest = read_info['earlistread']
    read_id = read_info['readlist'].split(",")[:-1]  # "a list"
    # read_time = results[4].split(",")[:-1]  # "a list"
    read_time = read_info['readtime']
    read_pop = read_info['readpop']
    if earliest == 0:
        earliest = read
    latest = read
    if str(stuid) not in read_id:
        read_id.append(str(stuid))
        read_id = ','.join(read_id) + ','   #a string
        read_pop = read_pop + 1

    read_time = read_time + str(stuid) + ':' + str(read) + ','
    result = update('update noteresponse set readList=?,readtime=?,earlistread=?,latestread=?,readpop=? where nid=?',
                    read_id, read_time, earliest, latest, read_pop, nid)
    # sql_all = "update noteresponse set readList='" + read_id + "'," + "readTime = '" + read_time + "',"\
    #           + "earlistRead = %d,latestRead = %d,readPop =%d where nID = %d;" % (earliest,latest,read_pop,nid)
    #
    # @mysql(sql_all)
    # def update(results=None):
    #     #log here
    #     return results
    # update()
    if result == 1:
        return 1
    else:
        return -1


def history_articles(stuid):
    send_info = select("select nid,stuids from noteindex")

    if not send_info:
        return None
    # sql = "select nid,stuids from noteindex"
    #
    # @mysql(sql)
    # def get(results=None):
    #     return results
    #
    # result = get()
    nids = [i['nid'] for i in send_info if str(stuid) in i['stuids']]
    # for i in result:
    #     if str(stuid) in i[1]:
    #         nids.append(i[0])
    articles = []
    article_dict = dict()
    article_dict['articles'] = dict()
    for x in nids:
        re = select_one('select nid,title,url from notecontent where nid =?', x)
        # sql = "select nid,title,url from notecontent where nid = %d" % x
        #
        # @mysql(sql)
        # def get_content(results=None):
        #     return results
        #
        # re = get_content()
        # articles.append(re)
        articles.append([re['nid'], re['title'], re['url']])
    return articles