# -*- coding:utf8 -*-
# Author: shizhenyu96@gamil.com
# github: https://github.com/imndszy
from nova_weixin.packages.novamysql import (select, select_int, select_one)


class Student(object):
    def __init__(self, openid):
        self.openid = openid
        self.Class = 100000
        self.stuid = get_stuid(openid)
        self.gpa = 5.0000
        self.gpa_rank = 100
        self.gpa_rank_next = 101
        self.gpa_rank_prev = 99
        self.routine = 100
        self.routine_base = 0
        self.routine_encou = 0
        self.routine_develop = 0
        self.routine_rank = 100
        self.stu_amount = 55
        self.tutor = '我'
        self.tutor_mail = 'imjtrszy@163.com'

    def get_routine_appraise(self):
        if self.stuid != -1:
            routine = select_one('select *from routine_appraise_13 where stuid = ?',self.stuid)
            if not routine:
                return "当前没有您的日常行为考核信息！"
            self.routine_base = routine['base']
            self.routine_encou = routine['encourage']
            self.routine_develop = routine['develop']
            self.routine = self.routine_base + self.routine_encou + self.routine_develop
            self.routine_rank = routine['rank']
            routine['total'] = self.routine
            return routine
        else:
            return "您尚未绑定学号！"

    def get_gpa(self):
        if self.stuid != -1:
            your_gpa = select_one('select *from creditcur where StuID = ?', self.stuid)

            if not your_gpa:
                return "当前没有您的GPA信息!!"
            if your_gpa.get('gpa'):
                self.gpa = round(your_gpa['gpa'], 4)
                self.Class = your_gpa['class']
                self.gpa_rank = your_gpa['rank']
                self.gpa_rank_next = self.gpa_rank + 1
                self.gpa_rank_prev = self.gpa_rank - 1

                max_rank = select_int('select max(rank) as max_rank from creditcur where class = ?',self.Class)

                your_gpa['max'] = max_rank
                if self.gpa_rank != max_rank:
                    next_gpa = select_one('select *from creditcur where Class = ? and rank= ?', self.Class, self.gpa_rank_next)

                    your_gpa['next'] = next_gpa['gpa']
                else:
                    your_gpa['nonnext'] = 1   # 排名是否最后的标志位
                    your_gpa['next'] = '悲剧…后面没有了'

                if self.gpa_rank_prev != 0:
                    prev_gpa = select_one('select *from creditcur where Class = ? and rank= ?', self.Class, self.gpa_rank_prev)

                    your_gpa['prev'] = prev_gpa['gpa']
                else:
                    your_gpa['nonprev'] = 1
                    your_gpa['prev'] = '很强！前面木有了'

                first_gpa = select_one('select *from creditcur where Class = ? and rank= ?', self.Class, 1)

                your_gpa['first'] = first_gpa['gpa']

                return your_gpa
            else:
                return '您没有记录在案的GPA数据！'
        else:
            return "您尚未绑定学号！"

    def get_recom(self):
        your_recom = self.get_gpa()
        if isinstance(your_recom, dict):
            maxRank = select_int('select MAX(rank) from creditcur where class=?',self.Class)

            your_recom['max_rank'] = maxRank
            self.stu_amount = your_recom['max_rank']
            if self.stu_amount:
                percent = self.stu_amount / 5
                result = select_int('select gpa from creditcur where class=? and rank=?',self.Class, percent)

                your_recom['twenty_per'] = result
        return your_recom

    def get_tutor(self):
        if self.stuid != -1:
            tutor = select_one('select *from tutor where StuID = ?', self.stuid)

            self.tutor = tutor['tutor']
            self.tutor_mail = tutor['mail']
            tutor_info = dict()
            tutor_info['status'] = 1
            tutor_info['same_tutor'] = []
            if self.tutor == '#N/A':
                tutor_info['status'] = 0
            else:
                temp = select('select *from tutor where tutor = ? and stuid <> ?', self.tutor, self.stuid)

                if temp:
                    tutor_info['same_tutor'] = temp
                    # [{},{}]
            return tutor_info
        else:
            return "您尚未绑定学号！"


def get_stuid(openid):
    stuid = select_int('select StuID from biding where OpenID =?', openid)

    if stuid:
        return stuid
    else:
        return None


def get_openid(stuid):
    openid = select_one('select openid from biding where stuid = ?', stuid)

    if openid:
        return openid['openid']
    else:
        return None


def get_stu_name(stuid):
    name = select_one('select name from stuinfo where stuid = ?', stuid)

    if name:
        return name['name']
    else:
        return None

def get_all_users():
    return select('select openid,stuid from biding ')
