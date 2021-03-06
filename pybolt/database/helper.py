import datetime
import decimal
import json
from pybolt.util.singleton import Singleton


class AchemyHelper(Singleton):
    def __init__(self):
        self.instance = None
        
    def set_instance(self, value):
        self.instance = value

    def dict_value_pad(self, key):
        if type(key) is type(int):
            return str(key)
        return "'" + str(key) + "'"

    def insert_from_dict(self, table, data):
        sql = 'INSERT INTO ' + table
        sql += ' ('
        sql += ', '.join(data)
        sql += ') VALUES ('
        sql += ', '.join(map(self.dict_value_pad, data.values()))
        sql += ');'
        return sql

    def update_from_dict(self, table, data, condition):
        sql = 'UPDATE ' + table
        sql += ' SET '
        count = 0
        for key, value in data.items():
            if count is not 0 and count < len(data) and value is not None:
                sql += ', '
            if type(value) is type(int):
                sql += "%s=%s" % (key, value)
            elif value == "CURRENT_TIMESTAMP":
                sql += "%s=%s" % (key, value)
            elif value is None:
                count += 1
                continue
            else:
                sql += "%s='%s'" % (key, value)
            count += 1
        sql += ' WHERE %s' % condition
        return sql
        
    def total_count(self, table):
        sql = "SELECT COUNT(*) FROM %s" % (table)
        result = self.instance.query(sql)
        if result is None:
            return -1
        return result[0][0]

    """
    def count(self, table, key, value):
        if isinstance(value, int):
            sql = "SELECT COUNT(*) FROM %s WHERE %s=%s" % (table, key, value)
        else:
            sql = "SELECT COUNT(*) FROM %s WHERE %s='%s'" % (table, key, value)
        result = self.instance.query(sql)
        if result is None:
            return -1
        return result[0][0]
    """

    def count(self, table, condition=None):
        sql = "SELECT COUNT(*) FROM %s %s" % (table, condition)
        result = self.instance.query(sql)
        if result is None:
            return -1
        return result[0][0]

    def alchemyencoder(self, obj):
        """JSON encoder function for SQLAlchemy special classes."""
        if isinstance(obj, datetime.date):
            return obj.isoformat()
        elif isinstance(obj, decimal.Decimal):
            return float(obj)
        return None

    def query_json(self, table, condition=None):
        if condition is not None:
            sql = "SELECT * FROM %s %s" % (table, condition)
        else:
            sql = "SELECT * FROM %s" % (table,)
        result = self.instance.query(sql)
        if result is None:
            return None
        dumps = json.dumps([dict(r) for r in result], default=self.alchemyencoder)
        decode = json.loads(dumps)
        if len(decode) == 0:
            return None
        return decode


alchemyhelper = AchemyHelper()
