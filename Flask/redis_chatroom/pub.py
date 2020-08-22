import redis
import sys
import json

config = {
    'host': '127.0.0.1',
    'port': 6379,
    'db': 0,
}

r = redis.StrictRedis(**config)

if __name__ == '__main__':
    name = 'EdgeNode'
    channel = 'Edge-to-UAV Channel'

    print('Welcome to', channel)

    while True:
        message = input('Enter a message: ')
        message=[1,3]
        if message == 'exit':
            break
        message=json.dumps(message)
        message=message.encode('utf-8')
        r.publish(channel, message)