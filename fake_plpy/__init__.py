import logging

class PlPy(object):

    def __init__(self, dsn=None, logger=None):
        if logger is None:
            logger = logging.getLogger(__name__)
        self.logger = logger
        if dsn is None:
            dsn = ''
        self.dsb = dsn

    def notice(self, message):
        self.logger.info(message)