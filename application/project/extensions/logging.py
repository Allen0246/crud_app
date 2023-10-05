import os
import logging
from logging.handlers import TimedRotatingFileHandler
from project.config.config import LOG_PATH, LOG_BACKUP_COUNT, LOG_LEVEL

def create_log_file(log_file_name):
    # if it does not exist then make a log folder
    if not os.path.exists(LOG_PATH):
        os.makedirs(LOG_PATH)

    log = logging.getLogger(log_file_name)
    log.setLevel(LOG_LEVEL)
    loggerStreamHandler = logging.StreamHandler()
    loggerStreamHandler.setLevel(LOG_LEVEL)

    logFormatter = logging.Formatter(
        '%(asctime)s [%(name)s] %(filename)-'
        '16s:%(lineno)-3d %(levelname)-8s %(message)s')
    loggerStreamHandler.setFormatter(logFormatter)
    log.addHandler(loggerStreamHandler)

    loggerfileHandler = TimedRotatingFileHandler(
        filename='{0}{1}.txt'.format(LOG_PATH,log_file_name),
        when='midnight',
        interval=1,
        encoding = "UTF-8",
        backupCount=LOG_BACKUP_COUNT)

    loggerfileHandler.suffix = '%Y%m%d.txt'
    loggerfileHandler.mode = 'a'
    loggerfileHandler.setFormatter(logFormatter)
    log.addHandler(loggerfileHandler)

    return log
