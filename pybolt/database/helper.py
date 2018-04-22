import datetime
import decimal
import json


class AchemyHelper:
    def __init__(self):
        print("AchemyHelper")
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
        sql += ', '.join(map(dict_value_pad, data.values()))
        sql += ');'
        return sql

    def update_from_dict(self, table, data, condition):
        sql = 'UPDATE ' + table
        sql += ' SET '
        count = 0

        for key, value in data.items():
            if type(value) is type(int):
                sql += "%s=%s" % (key, value)
            else:
                sql += "%s='%s'" % (key, value)
            if count < len(data)-1:
                sql += ', '
            count += 1

        sql += ' WHERE %s' % condition
        return sql

    def count_str(self, table, key, value):
        sql = "SELECT COUNT(*) FROM %s WHERE %s='%s'" % (table, key, value)
        result = self.instance.query(sql)
        return result[0][0]

    def count_int(self, table, key, value):
        sql = "SELECT COUNT(*) FROM %s WHERE %s=%s" % (table, key, value)
        result = self.instance.query(sql)
        return result[0][0]

    def alchemyencoder(self, obj):
        """JSON encoder function for SQLAlchemy special classes."""
        if isinstance(obj, datetime.date):
            return obj.isoformat()
        elif isinstance(obj, decimal.Decimal):
            return float(obj)
        return None

    def query_json(self, table, condition):
        sql = "SELECT * FROM %s WHERE %s" % (table, condition)
        result = self.instance.query(sql)
        dumps = json.dumps([dict(r) for r in result], default=self.alchemyencoder)
        decode = json.loads(dumps)
        if len(decode) == 0:
            return None
        return decode
        # return json.dumps(decode[0])

alchemyhelper = AchemyHelper()
