import logging
import datetime

log_file = ''


def get_log_file_name():
    return log_file


def get_logger():
    """
    :return: Logger that outputs both to the console and a log file
    """
    logger = logging.getLogger('gtfs_monthly_update')
    logger.setLevel(logging.DEBUG)
    # create file handler which logs even debug messages
    global log_file
    log_file = 'Transit Israel Monthly Update_' + datetime.datetime.now().strftime("%d%m%Y_%H%M") + '.txt'
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
