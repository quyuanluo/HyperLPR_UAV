import requests
import time
import json
import redis
import threading


def send_message(msg):   
    user_info = {'client_name': 'LAPTOP','msg_content':msg}  
    headers = {'content-type': 'application/json'}  
    resp_message = requests.post('http://10.0.0.214:6379/device/request_message', json=user_info, headers=headers)   
    return resp_message.json()['msg_content']

def listen_task():
    for item in ps.listen():
            print(item)   
    
if __name__ == '__main__':

    return_msg=send_message('Hello World!')
    print(return_msg)

    redis_conn = redis.StrictRedis(host='10.0.0.214',port=6379, db=0,)
    channel = 'Edge-to-UAV Channel'
    ps = redis_conn.pubsub()
    ps.subscribe(channel)
    print('Listening to', channel)

    thread = threading.Thread(target=listen_task)
    thread.setDaemon(True)
    thread.start()

    while True:
        requests.post('http://10.0.0.214:6379/pubsub')
        
