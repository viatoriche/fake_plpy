import logging
import psycopg2

class PlPy(object):

    def __init__(self, dsn=None, logger=None):
        if logger is None:
            logger = logging.getLogger(__name__)
        self.logger = logger
        if dsn is None:
            dsn = ''
        self.dsn = dsn
        self.db = psycopg2.connect(dsn=self.dsn)
        self.cursor = self.db.cursor()

    def notice(self, message):
        self.logger.info(message)


    def execute(self, *args, **kwargs):
        return self.cursor.execute(*args, **kwargs)

    def prepare(self, *args, **kwargs):
        return self.cursor.prepare(*args, **kwargs)