import datetime
import decimal
import json


def dict_value_pad(key):
    if type(key) is type(int):
        return str(key)
    return "'" + str(key) + "'"


def insert_from_dict(table, data):
    sql = 'INSERT INTO ' + table
    sql += ' ('
    sql += ', '.join(data)
    sql += ') VALUES ('
    sql += ', '.join(map(dict_value_pad, data.values()))
    sql += ');'
    return sql


def update_from_dict(table, data, condition):
    sql = u'UPDATE ' + table
    sql += u' SET '
    count = 0

    for key, value in data.items():
        if type(value) is type(int):
            sql += u"%s=%s" % (key, value)
        else:
            sql += u"%s='%s'" % (key, value)
        if count < len(data)-1:
            sql += ', '
        count += 1

    sql += u' WHERE %s' % condition
    return sql


def count_str(instance, table, key, value):
    sql = "SELECT COUNT(*) FROM %s WHERE %s='%s'" % (table, key, value)
    result = instance.query(sql)
    return result[0][0]


def count_int(instance, table, key, value):
    sql = "SELECT COUNT(*) FROM %s WHERE %s=%s" % (table, key, value)
    result = instance.query(sql)
    return result[0][0]



def alchemyencoder(obj):
    """JSON encoder function for SQLAlchemy special classes."""
    if isinstance(obj, datetime.date):
        return obj.isoformat()
    elif isinstance(obj, decimal.Decimal):
        return float(obj)
    return None


def query_json(instance, table, condition):
    sql = "SELECT * FROM %s WHERE %s" % (table, condition)
    result = instance.query(sql)
    dumps = json.dumps([dict(r) for r in result], default=alchemyencoder)
    decode = json.loads(dumps)
    return json.dumps(decode[0])
