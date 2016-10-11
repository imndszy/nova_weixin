# -*- coding:utf8 -*-
# Author: shizhenyu96@gamil.com
# github: https://github.com/imndszy
text_rep = "<xml>\
            <ToUserName><![CDATA[%s]]></ToUserName>\
            <FromUserName><![CDATA[%s]]></FromUserName>\
            <CreateTime>%s</CreateTime>\
            <MsgType><![CDATA[text]]></MsgType>\
            <Content><![CDATA[%s]]></Content>\
            </xml>"

image_rep = "<xml>\
             <ToUserName><![CDATA[%s]]></ToUserName>\
             <FromUserName><![CDATA[%s]]></FromUserName>\
             <CreateTime>%s</CreateTime>\
             <MsgType><![CDATA[image]]></MsgType>\
             <Image>\
             <MediaId><![CDATA[%s]]></MediaId>\
             </Image>\
             </xml>"

voice_rep = "<xml>\
             <ToUserName><![CDATA[%s]]></ToUserName>\
             <FromUserName><![CDATA[%s]]></FromUserName>\
             <CreateTime>%s</CreateTime>\
             <MsgType><![CDATA[voice]]></MsgType>\
             <Voice>\
             <MediaId><![CDATA[%s]]></MediaId>\
             </Voice>\
             </xml>"

video_rep = "<xml>\
            <ToUserName><![CDATA[%s]]></ToUserName>\
            <FromUserName><![CDATA[%s]]></FromUserName>\
            <CreateTime>%s</CreateTime>\
            <MsgType><![CDATA[video]]></MsgType>\
            <Video>\
            <MediaId><![CDATA[%s]]></MediaId>\
            <Title><![CDATA[%s]]></Title>\
            <Description><![CDATA[%s]]></Description>\
            </Video> \
            </xml>"

music_rep = "<xml>\
            <ToUserName><![CDATA[%s]]></ToUserName>\
            <FromUserName><![CDATA[%s]]></FromUserName>\
            <CreateTime>%s</CreateTime>\
            <MsgType><![CDATA[music]]></MsgType>\
            <Music>\
            <Title><![CDATA[%s]]></Title>\
            <Description><![CDATA[%s]]></Description>\
            <MusicUrl><![CDATA[%s]]></MusicUrl>\
            <HQMusicUrl><![CDATA[%s]]></HQMusicUrl>\
            <ThumbMediaId><![CDATA[%s]]></ThumbMediaId>\
            </Music>\
            </xml>"

news_rep_front = "<xml>\
                <ToUserName><![CDATA[%s]]></ToUserName>\
                <FromUserName><![CDATA[%s]]></FromUserName>\
                <CreateTime>%s</CreateTime>\
                <MsgType><![CDATA[news]]></MsgType>\
                <ArticleCount>%d</ArticleCount>\
                <Articles>"

news_rep_middle = "<item>\
                <Title><![CDATA[%s]]></Title>\
                <Description><![CDATA[%s]]></Description>\
                <PicUrl><![CDATA[%s]]></PicUrl>\
                <Url><![CDATA[%s]]></Url>\
                </item>"

news_rep_back = "</xml>"
