import logging


class ColoredFormatter(logging.Formatter):
    def format(self, record):
        if record.levelno == logging.WARNING:
            record.msg = '\033[93m%s\033[0m' % record.msg
        elif record.levelno == logging.ERROR:
            record.msg = '\033[91m%s\033[0m' % record.msg
        elif record.levelno == logging.INFO:
            record.msg = '\033[92m%s\033[0m' % record.msg
        return logging.Formatter.format(self, record)
