# -*- coding:utf8 -*-
# Author: shizhenyu96@gamil.com
# github: https://github.com/imndszy

APP_ID = 'wx92a9c338a5d02f38'
SECRET = 'aed361bef86c682fcc4f49db2df58588'
TOKEN = ''
TEMPLATE_ID = ''
MENU = {
    "button": [
        {

            "name": "通知消息",
            "sub_button": [
                {
                    "type": "click",
                    "name": "未读消息",
                    "key": "not_read_mes"
                },
                {
                    "type": "click",
                    "name": "历史消息",
                    "key": "history_mes"
                },
                {
                    "type": "click",
                    "name": "近期消息",
                    "key": "recent_mes"
                }]

        },
        {
            "name": "个人查询",
            "sub_button": [
                {
                    "type": "click",
                    "name": "日常考核",
                    "key": "daily_assess"
                },
                {
                    "type": "click",
                    "name": "绩点查询",
                    "key": "gpa"
                },
                {
                    "type": "click",
                    "name": "推免查询",
                    "key": "recom"
                },
                {
                    "type": "click",
                    "name": "导师查询",
                    "key": "tutor"
                }
            ]
        },
        {
            "name": "个性服务",
            "sub_button": [
                {
                    "type": "view",
                    "name": "微信问问",
                    "url": "http://121.42.216.141"
                },
                {
                    "type": "view",
                    "name": "教务推送",
                    "url": "http://121.42.216.141"
                },
                {
                    "type": "scancode_push",
                    "name": "扫码推事件",
                    "key": "rselfmenu_0_1",
                    "sub_button": []
                }
            ]

        }

    ]
}


