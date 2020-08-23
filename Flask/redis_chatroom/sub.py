import sys
import redis
import json

config = {
    'host': '10.0.0.120',
    'port': 6379,
    'db': 0,
}

r = redis.StrictRedis(**config)

if __name__ == '__main__':
    channel = 'Edge-to-UAV Channel'

    pubsub = r.pubsub()
    pubsub.subscribe(channel)

    print('Listening to', channel)

    while True:
        for item in pubsub.listen():
            data=item['data']
            if isinstance(data,int):
                print(data)
            elif isinstance(data,bytes):
                data=json.loads(data.decode('utf-8'))
                print(type(data),data)
