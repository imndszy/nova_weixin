# -*- coding:utf8 -*-
# Author: shizhenyu96@gamil.com
# github: https://github.com/imndszy
from lib.database import mysql


class Student(object):
    def __init__(self, openid):
        self.openid = openid
        self.Class = 100000
        
        # def get_stuid(openid):
        #     sql = "select StuID from biding where OpenID = '"+openid+"'"
        #     @mysql(sql)
        #     def get(results=''):
        #         if results:
        #             stuid = results[0]
        #             return stuid
        #         else:
        #             stuid = "NOT_IN_LIST"
        #             return stuid
        #     return get()
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
            sql = "select *from routine_appraise_13 where StuID = %d" % self.stuid

            @mysql(sql)
            def get_routine_appraise(results=''):
                return {'base': results[2], 'encourage': results[3], 'develop': results[4], 'rank': results[5]}
            routine = get_routine_appraise()
            self.routine_base = routine['base']
            self.routine_encou = routine['encourage']
            self.routine_develop = routine['develop']
            self.routine = self.routine_base+self.routine_encou+self.routine_develop
            self.routine_rank = routine['rank']
            routine['total'] = self.routine
            return routine
        else:
            return "您尚未绑定学号！"
    
    def get_gpa(self):
        if self.stuid != -1:
            sql = "select *from creditcur where StuID = %d" % self.stuid

            @mysql(sql)
            def get1(results=''):
                return {'class': results[1], 'gpa': results[4], 'rank': results[5]}
            your_gpa = get1()
            if your_gpa['gpa']:
                self.gpa = round(your_gpa['gpa'], 4)
                self.Class = your_gpa['class']
                self.gpa_rank = your_gpa['rank']
                self.gpa_rank_next = self.gpa_rank+1
                self.gpa_rank_prev = self.gpa_rank-1
                
                sql = "select *from creditcur where Class = %d and rank= %d" % (self.Class, self.gpa_rank_next)

                @mysql(sql)
                def get2(results=''):
                    if results:
                        return {'gpa': results[4]}
                    else:
                        return {'gpa': 'NONE_ELE'}
                next_gpa = get2()
                your_gpa['next'] = next_gpa['gpa']
                
                sql = "select *from creditcur where Class = %d and rank= %d" % (self.Class, self.gpa_rank_prev)

                @mysql(sql)
                def get3(results=''):
                    if results:
                        return {'gpa': results[4]}
                    else:
                        return {'gpa': 'NONE_ELE'}
                prev_gpa = get3()
                your_gpa['prev'] = prev_gpa['gpa']
                
                sql = "select *from creditcur where Class = %d and rank= %d" % (self.Class, 1)

                @mysql(sql)
                def get4(results=''):
                    if results:
                        return {'gpa': results[4]}
                    else:
                        return {'gpa': 'NONE_ELE'}
                first_gpa = get4()
                your_gpa['first'] = first_gpa['gpa']
                
                sql = "select max(rank) as max_rank from creditcur where class = %d" % self.Class

                @mysql(sql)
                def get5(results=''):
                    return results[0]
                max_rank = get5()
                your_gpa['max'] = max_rank
                return your_gpa
            else:
                return '您没有记录在案的GPA数据！'
        else:
            return "您尚未绑定学号！"
        
    def get_recom(self):
        your_recom = self.get_gpa()
        if isinstance(your_recom, dict):
            sql = "select MAX(rank) from creditcur where Class = %d" % self.Class

            @mysql(sql)
            def get2(results=''):
                if results:
                    return {'max_rank': results[0]}
                else:
                    return {'max_rank': ''}
            max_rank = get2()
            your_recom['max_rank'] = max_rank['max_rank']
            self.stu_amount = your_recom['max_rank']
            if self.stu_amount:
                percent = self.stu_amount/5
                sql = "select *from creditcur where Class = %d and rank= %d" % (self.Class, percent)

                @mysql(sql)
                def get(results=''):
                    if results:
                        return {'20gpa': results[4]}
                    else:
                        return {'20gpa': ''}
                your_recom['twenty_per'] = get()['20gpa']
        return your_recom

    def get_tutor(self):
        if self.stuid != -1:
            sql = "select *from tutor where StuID = %d" % self.stuid

            @mysql(sql)
            def get(results=''):
                return {'tutor_mail': results[6], 'tutor': results[5]}
            tutor = get()
            self.tutor = tutor['tutor']
            self.tutor_mail = tutor['tutor_mail']
            tutor_info = dict()
            tutor_info['status'] = 1
            tutor_info['same_tutor'] = []
            if self.tutor == '#N/A':
                tutor_info['status'] = 0
            else:
                sql = "select *from tutor where tutor = '"+self.tutor+"' and stuid <> %d" % self.stuid

                @mysql(sql)
                def get1(results=''):
                    return results
                if get1():
                    tutor_info['same_tutor'] = get1()
                else:
                    tutor_info['same_tutor'] = []
            
            return tutor_info
        else:
            return "您尚未绑定学号！"


def get_stuid(openid):
    sql = "select StuID from biding where OpenID = '"+openid+"'"

    @mysql(sql)
    def get(results=''):
        if results:
            stuid = results[0]
            return stuid
        else:
            # stuid = "NOT_IN_LIST"
            return -1
    return get()


def get_openid(stuid):
    sql = "select openid from biding where stuid = '"+stuid+"'"

    @mysql(sql)
    def get(results=''):
        if results:
            openid = results[0]
            return openid
        else:
            return -1
    return get()
