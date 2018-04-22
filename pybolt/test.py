import datetime
import decimal
import json
import logging
from sqlalchemy import exc
import log.rotation_log
from bcrypt.crypto_manager import AESCipher
from database.alchemy_pool import thealchemy

def alchemyencoder(obj):
    """JSON encoder function for SQLAlchemy special classes."""
    if isinstance(obj, datetime.date):
        return obj.isoformat()
    elif isinstance(obj, decimal.Decimal):
        return float(obj)
    return None

# test = None
test = "database"
# test = "log"
# test = "crypto"

if test == "crypto":
    shakey = b'abcdefghijklmnopqrstuvwxyz123456'

    message = 'Good Morning, Python'
    # message = 'abcdefghijklmnopqrstuvwxyz123456'
    # message = '1234567890123456'
    # message = u'한글을 테스트 합니다.'

    encval = AESCipher(shakey).encrypt(message, 'ECB', 'ZEROS')
    decval = AESCipher(shakey).decrypt(encval, 'ECB', 'ZEROS')

    print("message :", message)
    print("encrypt :", encval)
    print("decrypt :", decval)

elif test == "database":
    connect_string = "%s://%s:%s@%s:%d/%s" % \
        ('mysql', 'fullpath', 'fullpath', 'localhost', 3306, 'fullpath')  # db, uid, pwd, host, port, dbname
    thealchemy.create_pool(connect_string, 0)
    try:
        sql = "SELECT * FROM member WHERE uid = 'keidw'"
        result = thealchemy.query(sql)
        dumps = json.dumps([dict(r) for r in result], default=alchemyencoder)
        decode = json.loads(dumps)
        print(json.dumps(decode[0]))
    except exc.DBAPIError:
        print("except")

elif test == "log":
    log.rotation_log.create_date_rotating_file_handler()
    logger = logging.getLogger()
    logger.info("TEST")

else:
    print("Hello, HighV Python Library")
