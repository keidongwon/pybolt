
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
