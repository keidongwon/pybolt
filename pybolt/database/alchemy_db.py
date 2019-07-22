from sqlalchemy import create_engine, inspect
from sqlalchemy.ext.declarative import declarative_base
import datetime

Base = declarative_base()

class AlchemyBase():
    def to_dict(self):
        result = {c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs}
        if result is None: 
            return None
        for item in result:
            if type(result[item]) == datetime.datetime:
                result[item] = datetime.datetime.strftime(result[item], "%Y-%m-%d %H:%M:%S")
        return result
