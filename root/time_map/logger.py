"""
Logger for logging info and error messages both to the console and logger file named
"Transit_israel_monthly_update_<current_date_time>.txt"

"""
import logging
import datetime
import os

log_file = ''


def get_log_file_name():
    """
    the name of the logging file
    :return:
    """
    return log_file


def get_logger():
    """
    :return: Logger that outputs both to the console and a log file
    """
    # logging.setLoggerClass(Logger) # Used to support python3 string formatting
    # logging.setLogRecordFactory(LogRecord)
    logger = logging.getLogger('gtfs_monthly_update')
    logger.setLevel(logging.DEBUG)
    # create file handler which logs even debug messages
    global log_file
    #check if logs fodler exists, and if not create it
    logs_folder_path = os.getcwd() + "/logs"
    if not os.path.exists(logs_folder_path):
        os.mkdir("logs")
    log_file = logs_folder_path + '/Transit_israel_monthly_update_' + datetime.datetime.now().strftime("%d%m%Y_%H%M") + '.txt'
    fh = logging.FileHandler(log_file)
    fh.setLevel(logging.NOTSET)
    # create console handler with a higher log level
    ch = logging.StreamHandler()
    ch.setLevel(logging.NOTSET)
    # ch1 = logging.StreamHandler()
    # create formatter and add it to the handlers
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)
    # ch1.setFormatter(formatter)
    fh.setFormatter(formatter)
    # add the handlers to logger
    logger.addHandler(ch)
    # logger.addHandler(ch1)
    logger.addHandler(fh)
    return logger
