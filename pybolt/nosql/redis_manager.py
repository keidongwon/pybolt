import traceback
import redis
# from redis.sentinel import Sentinel


class BeRedis:
    def __init__(self, host='localhost', port=6379, pwd=None, master=None):
        self.pool = None
        self.host = host
        self.port = port
        self.pwd = pwd
        self.master = master
        # self.sentinel = None

    def create_pool(self):
        try:
            if self.pool:
                self.pool.disconnect()
                self.pool.reset()

            self.pool = redis.ConnectionPool(host=self.host, port=self.port, password=self.pwd)

        except redis.ConnectionError as e:
            print("except : {}\n{}".format(e, traceback.format_exc()))

    def object(self):
        rds = None
        if not self.pool:
            return rds

        try:
            rds = redis.Redis(connection_pool=self.pool)
            rds.ping()

        except redis.ConnectionError as e:
            print("except : {}\nReconnect redis.".format(e))
            self.create_pool()
            rds = self.object()

        return rds


# for test
if __name__ == '__main__':
    _rds = BeRedis()
    _rds.create_pool()
    rds_obj = _rds.object()
    print(rds_obj.ping())
    print('Test Done!')
