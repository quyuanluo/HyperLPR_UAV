#!-*-encoding:utf-8-*-

import redis

class Task(object):

    def __init__(self, redis_conn=None):
        self.rcon = redis_conn
        self.queue = 'task:prodcons:queue'

    def listen_task(self):
        while True:
            task = self.rcon.blpop(self.queue, 0)[1]
            print("Task get", task)


if __name__ == '__main__':
    print('listen task queue')
    pool = redis.ConnectionPool(host='10.0.0.214',
                                port=5000, db=5)
    redis_conn = redis.StrictRedis(connection_pool=pool)
    Task(redis_conn=redis_conn).listen_task()