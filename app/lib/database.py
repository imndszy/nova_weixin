# -*- coding:utf8 -*-
# Author: shizhenyu96@gamil.com
# github: https://github.com/imndszy
import functools
import MySQLdb
import logging

from nova_weixin.app.config import (DB_HOSTNAME, DB_NAME,
                                    DB_PASSWORD, DB_USERNAME)


def mysql(sql):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            try:
                conn = MySQLdb.connect(host=DB_HOSTNAME,
                                       user=DB_USERNAME, passwd=DB_PASSWORD,
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
            except MySQLdb.Error as e:
                logging.basicConfig(format='%(asctime)s %(message)s',
                                    datefmt='%Y/%m/%d %I:%M:%S %p',
                                    filename='./log/database.log',
                                    level=logging.DEBUG)
                logging.debug("Mysql Error %d:%s" % (e.args[0], e.args[1]))
                return -1
        return wrapper
    return decorator
