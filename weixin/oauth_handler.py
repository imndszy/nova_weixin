# -*- coding:utf8 -*-
# Author: shizhenyu96@gamil.com
# github: https://github.com/imndszy
import json
import urllib2
import config
from nova.get_user_info import get_stuid


def get_openid(code):
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
          "appid=%s&secret=%s&code=%s&grant_type=authorization_code" % (config.APP_ID, config.SECRET, code)
    result = urllib2.urlopen(url).read()
    return json.loads(result)['openid']


def openid_handler(openid, post_url):
    """
    update the mysql database using openid and post_url
    :param openid: openid of the user who read the specific article
    :param post_url: the url of the article
    :return: return the result of the mysql's update
    """
    stuid = get_stuid(openid)

