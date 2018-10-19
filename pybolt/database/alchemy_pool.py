import datetime
import decimal
import logging
import json
from sqlalchemy import create_engine
from sqlalchemy import exc
from sqlalchemy import text
from pybolt.util.singleton import Singleton

# logger = logging.getLogger()


class AlchemyPool(Singleton):
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
    def create_pool(self, connect_string, poolsize=10):
        # global engine
        if poolsize == 0 or poolsize == 1:
            self.engine = create_engine(connect_string)
        else:
            self.engine = \
                create_engine(connect_string, pool_size=poolsize,
                              pool_recycle=3600, max_overflow=0)

    # @staticmethod
    def get_connection(self):
        # global engine
        return self.engine.connect()

    # @staticmethod
    def execute(self, sql):
        result = True
        try:
            # sql = sql.encode('utf-8')
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
    def insert(self, sql):
        result = True
        try:
            conn = self.get_connection()
            trans = conn.begin()
            proxy = conn.execute(sql)
            trans.commit()
            result = proxy.lastrowid
        except exc.DBAPIError as e:
            result = False
            trans.rollback()
            print("except : ", e)
        finally:
            conn.close()
        return result

    # @staticmethod
    def query(self, sql, like=None):
        try:
            conn = self.get_connection()
            if like is None:
                return conn.execute(sql).fetchall()
            else:
                return conn.execute(text(sql), value=like).fetchall()
        except exc.DBAPIError as e:
            print("except : ", e)
        finally:
            conn.close()

    # @staticmethod
    def query_json(self, sql, like=None):
        result = self.query(sql, like)
        if result is None:
            return None
        else:
            return json.dumps([dict(r) for r in result], default=AlchemyPool.alchemyencoder)

thealchemy = AlchemyPool()
