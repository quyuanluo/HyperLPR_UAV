#!-*-encoding:utf-8-*-

import redis

class Task(object):

    def __init__(self, redis_conn,channel):
        self.rcon = redis_conn
        self.ps = self.rcon.pubsub()
        self.ps.subscribe('task:pubsub:%s' % channel)

    def listen_task(self):
        for i in self.ps.listen():
            if i['type'] == 'message':
                print("Task get ", i["data"])

if __name__ == '__main__':
    print("listen task channel")

    pool = redis.ConnectionPool(host='10.0.0.214',
                                port=5000, db=5,)

    redis_conn = redis.StrictRedis(connection_pool=pool)
    Task(redis_conn, 'channel').listen_task()