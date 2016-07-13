# -*- coding:utf8 -*- 
# Author: shizhenyu96@gamil.com
# github: https://github.com/imndszy
import functools
import MySQLdb
from config import DB_HOSTNAME, DB_NAME, DB_PASSWORD, DB_USERNAME


def mysql(sql):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            try:
                conn = MySQLdb.connect(host=DB_HOSTNAME, user=DB_USERNAME, passwd=DB_PASSWORD,
                                       db=DB_NAME, charset='utf8')
                cursor = conn.cursor()
                count = cursor.execute(sql)
                if count <= 1:
                    info = cursor.fetchone()
                    if info:
                        results = list(info)
                    else:
                        results = []
                else:
                    info = cursor.fetchall()
                    results = list(info)
                kwargs['results'] = results
                result = func(*args, **kwargs)
                conn.commit()
                cursor.close()
                conn.close()
                return result
            except MySQLdb.Error, e:
                return -1 #"Mysql Error %d:%s" % (e.args[0],e.args[1])
        return wrapper
    return decorator


# class Mysql:
#     def __init__(self, database):
#         self.database = database
#
#     def add(self, table, alist):
#         """
#         :param table: the mysql table
#         :param alist: a list contains a line of data which will be inserted into the table
#         :return:whether the operation is right
#         """
#         pass
#
#     def update(self, table, adict):
#         pass
#
#     def get(self, table, requirement, column=None):
#         if column:
#             sql = "select from %s where %s" % (table, requirement)
#         else:
#             sql = "select * from %s where %s" % (table, requirement)
#
#         @mysql(sql)
#         def get_mysql(results=''):
#             return results
#         result = get_mysql()
#         if len(result) == 0:
#             return None
#         else:
#             return result
#
#     def addmany(self, table, alist):
#         pass

if __name__ == "__main__":
    print("___")
