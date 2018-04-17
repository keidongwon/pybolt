import codecs
import os
import sys
import socket
import time
import logging
from logging.handlers import TimedRotatingFileHandler


class DateRotatingFileHandler(TimedRotatingFileHandler):
    def __init__(self, path, log_name, ip, ext):
        self.path = path
        self.log_name = log_name
        self.ip = ip
        self.ext = ext

        self.baseFilename = self.get_filename()
        logging.handlers.TimedRotatingFileHandler.__init__(self,
                                                           self.baseFilename,
                                                           when='midnight',
                                                           interval=1,
                                                           backupCount=4,
                                                           encoding='utf-8')

    def doRollover(self):
        self.stream.close()
        self.baseFilename = self.get_filename()
        if self.encoding:
            self.stream = codecs.open(self.baseFilename, 'a', self.encoding)
        else:
            self.stream = open(self.baseFilename, 'a')

    def get_filename(self):
        if not self.ip:
            return "%s/%s-%s.%s" % (self.path, time.strftime("%Y%m%d"), self.log_name, self.ext)
        else:
            return "%s/%s-%s-%s.%s" % \
                (self.path, time.strftime("%Y%m%d"), self.log_name, self.ip, self.ext)


def create_date_rotating_file_handler(ip_flag=False,
                                      log_path=None,
                                      log_name=None,
                                      log_format=None,
                                      log_level=None,
                                      console=False,
                                      ext='log'):

    path = log_path or os.path.dirname(os.path.abspath(__file__))
    lformat = log_format or logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    name = log_name or os.path.basename(sys.argv[0]).replace(".py", "")
    level = log_level or logging.DEBUG

    ip = socket.gethostbyname(socket.gethostname()) if ip_flag else None
    handler = DateRotatingFileHandler(path, name, ip, ext)
    handler.setFormatter(lformat)

    logger = logging.getLogger()
    logger.addHandler(handler)
    logger.setLevel(level)

    if console:
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(lformat)
        logger.addHandler(console_handler)
