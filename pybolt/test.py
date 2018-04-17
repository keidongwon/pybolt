import datetime
import decimal
import json
import logging
from sqlalchemy import exc
import log.rotation_log
from bcrypt.crypto_manager import AESCipher
from database.alchemy_pool import AlchemyPool


def alchemyencoder(obj):
    """JSON encoder function for SQLAlchemy special classes."""
    if isinstance(obj, datetime.date):
        return obj.isoformat()
    elif isinstance(obj, decimal.Decimal):
        return float(obj)
    return None

# test = None
# test = "database"
# test = "log"
test = "crypto"

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
        ('mysql', 'keidw', 'dkdiskal', 'localhost', 3306, 'company')
    AlchemyPool.create_pool(connect_string, 0)
    try:
        sql = "SELECT * FROM member WHERE uid = 'tetris'"
        ret = AlchemyPool.query(sql)
        result = json.dumps([dict(r) for r in ret], default=alchemyencoder)
        decode = json.loads(result)
        print(json.dumps(decode[0]))
    except exc.DBAPIError:
        print("except")

elif test == "log":
    log.rotation_log.create_date_rotating_file_handler()
    logger = logging.getLogger()
    logger.info("TEST")

else:
    print("Hello, HighV Python Library")
