# -*- coding:utf8 -*-
# Author: shizhenyu96@gamil.com
# github: https://github.com/imndszy
import logging

class NovaLog:
    def __init__(self, path, level = logging.DEBUG):
        self.logger = logging.getLogger(path)
        self.logger.setLevel(logging.DEBUG)
        fmt = logging.Formatter('%(asctime)s - %(filename)s - %(levelname)s - %(message)s')

        #设置文件日志
        fh = logging.FileHandler(path)
        fh.setFormatter(fmt)
        fh.setLevel(level)
        self.logger.addHandler(fh)

    def debug(self,message):
        self.logger.debug(message)

    def info(self,message):
        self.logger.info(message)

    def warn(self,message):
        self.logger.warn(message)

    def error(self,message):
        self.logger.error(message)

    def critical(self,message):
        self.logger.critical(message)


if __name__ =='__main__':
    log = NovaLog('a.log',logging.DEBUG)
    log.debug('一个debug信息')
    log.info('一个info信息')
    log.warn('一个warning信息')
    log.error('一个error信息')
    log.critical('一个致命critical信息')
