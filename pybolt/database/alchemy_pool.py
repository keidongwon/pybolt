import datetime
import decimal
import logging
import json
from sqlalchemy import create_engine
from sqlalchemy import exc

# engine = None
logger = logging.getLogger()


class AlchemyPool:
    def __init__(self):
        self.engine = None

    @staticmethod
    def alchemyencoder(obj):
        """JSON encoder function for SQLAlchemy special classes."""
        if isinstance(obj, datetime.datetime):
            return obj.isoformat(' ')
        elif isinstance(obj, datetime.date):
            return obj.isoformat()
        elif isinstance(obj, decimal.Decimal):
            return float(obj)
        return None

    # @staticmethod
    # def create_pool(connect_string, poolsize=10):
    def create_pool(self, connect_string, poolsize=10):
        # global engine
        if poolsize == 0 or poolsize == 1:
            self.engine = create_engine(connect_string)
        else:
            self.engine = \
                create_engine(connect_string, pool_size=poolsize, pool_recycle=3600, max_overflow=0)

    # @staticmethod
    # def get_connection():
    def get_connection(self):
        # global engine
        return self.engine.connect()

    # @staticmethod
    # def execute(sql):
    def execute(self, sql):
        result = True
        try:
            sql = sql.encode('utf-8')
            conn = self.get_connection()
            trans = conn.begin()
            conn.execute(sql)
            trans.commit()
        except exc.DBAPIError as e:
            result = False
            trans.rollback()
            print("except : ", e)
        finally:
            conn.close()
        return result

    # @staticmethod
    # def query(sql):
    def query(self, sql):
        try:
            conn = self.get_connection()
            return conn.execute(sql).fetchall()
        except exc.DBAPIError as e:
            print("except : ", e)
        finally:
            conn.close()

    # @staticmethod
    # def query_json(sql):
    def query_json(self, sql):
        result = self.query(sql)
        return json.dumps([dict(r) for r in result], default=AlchemyPool.alchemyencoder)

thealchemy = AlchemyPool()
