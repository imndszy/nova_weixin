# -*- coding:utf8 -*- 
# Author: shizhenyu96@gamil.com
# github: https://github.com/imndszy
import MySQLdb
import functools
import config


def mysql(sql):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            conn = MySQLdb.connect(host=config.DB_HOSTNAME, user=config.DB_USERNAME, passwd=config.DB_PASSWORD,
                                   db=config.DB_NAME)
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
            cursor.close()
            conn.close()
            return result
        return wrapper
    return decorator

if __name__ == "__main__":
    print("___")