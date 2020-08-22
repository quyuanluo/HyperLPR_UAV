#!/usr/bin/env python
# encoding: utf-8
"""
@version: v1.0
@author: W_H_J
@license: Apache Licence
@contact: 415900617@qq.com
@software: PyCharm
@file: flaskIOTest.py
@time: 2019/2/20 12:04
@describe: flask-socketio 服务端
"""
import sys
import os
import json
sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/' + '..'))
sys.path.append("..")
from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit
 
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO()
socketio.init_app(app)
 
name_space = '/test'
 
 
@app.route('/')
def get_abc():
    """加载接收消息页面"""
    return render_template('index.html')
 
 
@app.route('/push')
def push_once():
    """广播消息
    发送消息：http://127.0.0.1:5000/push?msg=a
    """
    event_name = 'message'
    data = request.args.get("msg")
    broadcasted_data = {'data': data}
    print("publish msg==>", broadcasted_data)
    socketio.emit(event_name, broadcasted_data, broadcast=True, namespace=name_space)
    msg=json.dumps({'pos':[1,3]})
    return msg
 
 
@socketio.on('recevice message', namespace=name_space)
def test_message(message):
    print('recevice message', message)
    # emit('message', {'data': message['data']})
 
 
@socketio.on('connect', namespace=name_space)
def connected_msg():
    """客户端连接"""
    print('client connected!', request.sid)
    socketio.emit('abcde', 'hello', namespace=name_space)
 
 
@socketio.on('disconnect', namespace=name_space)
def disconnect_msg():
    """客户端离开"""
    print('client disconnected!')
 
 
if __name__ == '__main__':
    print("conent http://127.0.0.1:5000")
    socketio.run(app,host='0.0.0.0', port=5000)