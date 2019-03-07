"""
Logger for logging info and error messages both to the console and logger file named
"Transit_israel_monthly_update_<current_date_time>.txt"

"""
import logging
import datetime
import os


class Logger(object):
    def __init__(self):
        self.log_name = ""
        self.log_file = ""
        self.log = None

    def get_logger_name(self):
        return self.log_file

    def get_logger(self, log_name):
        """
        :return: Logger that outputs both to the console and a log file
        """
        if self.log is not None:
            return self.log
        self.log_name = log_name
        logger = logging.getLogger(log_name)
        logger.setLevel(logging.DEBUG)
        # create file handler which logs even debug messages
        # check if logs fodler exists, and if not create it
        logs_folder_path = os.path.join(os.getcwd(), "logs")
        if not os.path.exists(logs_folder_path):
            os.mkdir("logs")
        self.log_file = os.path.join(logs_folder_path, log_name + datetime.datetime.now().strftime("%d%m%Y_%H%M") + '.txt')
        fh = logging.FileHandler(self.log_file)
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
        self.log = logger
        return self

    def info(self, msg):
        self.log.info(msg)

    def error(self, msg):
        self.log.error(msg)

    def debug(self, msg):
        self.log.debug(msg)

    def exception(self,msg):
        self.log.exception(msg)


_log = Logger()
_log = _log.get_logger("Transit Analyst")
