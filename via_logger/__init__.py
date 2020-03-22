import logging
from colored import fg, attr
from typing import List
from .utils import *


class BeautifulFormatter(logging.Formatter):

    warning_color = fg('yellow')
    error_color = fg('red')
    critical_color = fg('red')
    info_color = fg('green')
    debug_color = fg('grey_93')
    default_color = fg('white')
    reset_color = attr('reset')

    def __init__(self):
        logging.Formatter.__init__(self,
                                   fmt='[%(asctime)s] {} %(levelname)s {}' +
                                   ' : %(message)s (%(pathname)s:%(lineno)d)',
                                   datefmt='%m/%d/%Y %I:%M:%S %p'
                                   )

    def format(self, record):
        original_format = self._fmt
        original_style_format = self._style._fmt

        def set_color(color):
            self._fmt = self._fmt.format(color, BeautifulFormatter.reset_color)
            self._style._fmt = self._style._fmt.format(
                color, BeautifulFormatter.reset_color)

        if record.levelno == logging.DEBUG:
            set_color(self.debug_color)
        elif record.levelno == logging.INFO:
            set_color(self.info_color)
        elif record.levelno == logging.WARNING:
            set_color(self.warning_color)
        elif record.levelno == logging.ERROR:
            set_color(self.error_color)
        elif record.levelno == logging.CRITICAL:
            set_color(self.critical_color)

        record = logging.Formatter.format(self, record)

        self._fmt = original_format
        self._style._fmt = original_style_format
        return record

    def get_decolorized(self):
        return logging.Formatter(self._fmt.format('', ''),
                                 datefmt='%m/%d/%Y %I:%M:%S %p')

    @staticmethod
    def create_formatter(color):
        return logging.Formatter('[ % (asctime)s] ' + color + '%(levelname)s' +
                                 BeautifulFormatter.reset_color +
                                 ': % (message)s ( % (pathname)s: % (lineno)d)',
                                 datefmt='%m/%d/%Y %I:%M:%S %p')


class BeautifulLogger:
    loggers: List[logging.Logger] = []

    def __init__(self):
        raise NotImplementedError(
            "Cannot initialize BeautifulLogger instance."
        )

    @staticmethod
    def get_instance(log_file: str) -> logging.Logger:
        # Return logger with the specified
        # file name if exists
        for logger in BeautifulLogger.loggers:
            for handler in BeautifulLogger.logger.handlers:
                if isinstance(handler, logging.FileHandler):
                    if handler.stream.name == log_file:
                        return logger
        logger = logging.getLogger(
            __name__ + str(len(BeautifulLogger.loggers)))
        logger.handlers.clear()
        logger.setLevel(logging.DEBUG)

        formatter = BeautifulFormatter()

        # logging to file
        logging_handler = logging.FileHandler(log_file)
        logging_handler.setFormatter(
            formatter.get_decolorized())
        logging_handler.setLevel(logging.DEBUG)
        logger.addHandler(logging_handler)

        # logging to console
        logging_console_handler = logging.StreamHandler()
        logging_console_handler.setFormatter(formatter)
        logging_console_handler.setLevel(logging.DEBUG)
        logger.addHandler(logging_console_handler)

        BeautifulLogger.loggers.append(logger)
        return logger
