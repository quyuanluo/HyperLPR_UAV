# coding=utf-8
'''
Created on 2015-9-9
@author: Administrator
'''
import redis
pool=redis.ConnectionPool(host='127.0.0.1',port=6379,db=0)
r = redis.StrictRedis(connection_pool=pool)
while True:
    input = input("publish:")
    if input == 'over':
        print ('停止发布')
        break
    r.publish('spub', input)