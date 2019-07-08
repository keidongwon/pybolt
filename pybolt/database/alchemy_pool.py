import datetime
import decimal
import logging
import json
from sqlalchemy import create_engine
from sqlalchemy import exc
from sqlalchemy import text
from pybolt.util.singleton import Singleton


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

    def create_pool(self, connect_string,
                    enc='utf8',
                    poolsize=5,
                    poolrecycle=-1,
                    maxoverflow=10):
        if poolsize == 0 or poolsize == 1:
            self.engine = create_engine(connect_string, encoding=enc)
        else:
            self.engine = \
                create_engine(connect_string,
                              encoding=enc,
                              pool_size=poolsize,
                              pool_recycle=poolrecycle,
                              max_overflow=maxoverflow)

    def get_connection(self):
        get_conn = None
        try:
            get_conn = self.engine.connect()
        except exc.DBAPIError as e:
            logging.getLogger().info("alchemy_pool.get_connection - exception : %s", e)
        return get_conn

    def execute(self, sql):
        result = True
        conn = None
        trans = None
        try:
            conn = self.get_connection()
            if conn is None:
                return None
            trans = conn.begin()
            conn.execute(sql)
            trans.commit()
        except exc.DBAPIError as e:
            result = False
            if trans is not None:
                trans.rollback()
            logging.getLogger().info("alchemy_pool.execute - exception : %s", e)
        finally:
            if conn is not None:
                conn.close()
        return result

    def insert(self, sql):
        result = None
        conn = None
        trans = None
        try:
            conn = self.get_connection()
            if conn is None:
                return result
            trans = conn.begin()
            proxy = conn.execute(sql)
            trans.commit()
            result = proxy.lastrowid
        except exc.DBAPIError as e:
            result = False
            if trans is not None:
                trans.rollback()
            logging.getLogger().info("alchemy_pool.insert - exception : %s", e)
        finally:
            if conn is not None:
                conn.close()
        return result

    def query(self, sql, like=None):
        conn = None
        try:
            conn = self.get_connection()
            if conn is None:
                return None
            if like is None:
                return conn.execute(sql).fetchall()
            else:
                return conn.execute(text(sql), value=like).fetchall()
        except exc.DBAPIError as e:
            logging.getLogger().info("alchemy_pool.query - exception : %s", e)
        finally:
            if conn is not None:
                conn.close()

    def query_json(self, sql, like=None):
        result = self.query(sql, like)
        if result is None:
            return None
        else:
            encode = json.dumps([dict(r) for r in result], default=AlchemyPool.alchemyencoder)
            decode = json.loads(encode)
            return decode


thealchemy = AlchemyPool()
