import logging
import random
import string
import unittest

import os
import sqlalchemy

logging.basicConfig(level=logging.DEBUG)

pg_dsn = os.environ.get('PGDSN', "postgresql://testdb:testdb@localhost/testdb")


def random_string(size=12, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


class TestFakePlPy(unittest.TestCase):
    def setUp(self):
        """create environment"""
        self.engine = sqlalchemy.create_engine(pg_dsn, echo=True)
        from sqlalchemy import Column, Integer, String
        from sqlalchemy.ext.declarative import declarative_base
        from sqlalchemy.orm import sessionmaker

        self.Session = sessionmaker()
        self.Session.configure(bind=self.engine)
        self.session = self.Session()

        Base = declarative_base()

        class TestModel(Base):
            __tablename__ = 'test'

            id = Column(Integer, primary_key=True, autoincrement=True)
            data1 = Column(String(1024))
            data2 = Column(String(1024))
            data3 = Column(String(1024))

            def __init__(self, **kwargs):
                for k in kwargs:
                    setattr(self, k, kwargs[k])

        self.TestModel = TestModel
        self.metadata = Base.metadata
        self.test_table = self.TestModel.__table__
        self.metadata.create_all(self.engine)
        test1 = self.TestModel(data1="test1_1", data2="test1_2", data3="test1_3")
        # create 5 random tests
        tests = [self.TestModel(data1=random_string(), data2=random_string(), data3=random_string()) for x in xrange(5)]
        self.session.add_all([test1] + tests)
        self.session.commit()

    def test_fake_plpy(self):
        from fake_plpy import PlPy

        logger = logging.getLogger(__name__)

        plpy = PlPy(logger=logger, dsn=pg_dsn)
        plpy.notice('test message')
        result = plpy.execute("SELECT * FROM 'test'")
        print 'RESULT', result

    def tearDown(self):
        """destroy environment"""
        self.test_table.drop(self.engine)
