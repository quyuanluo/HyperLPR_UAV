from flask import Flask, jsonify, request
import os
import time
import json
import redis

redis_conn = redis.StrictRedis(host='10.0.0.214',port=6379, db=0,)
channel = 'Edge-to-UAV Channel'

app = Flask(__name__)

@app.route('/')
def index():
    return 'Hello,welcome to the edge computing server!'

@app.route('/device/request_message', methods=['POST'])
def handle_message():  
    msg_data=request.json
    print(msg_data)
    return jsonify(msg_data)

@app.route('/pubsub',methods=['POST'])
def pubsub():
    redis_conn.publish(channel, "received your subscribe!")
    return True


if __name__ == '__main__':
    app.run(debug=True,host='10.0.0.214',port=6379)
    
        