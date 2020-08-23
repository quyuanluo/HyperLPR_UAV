# 服务端接收请求时，用request.json
# 将传过来的JSON type的数据转化成字典类型

from flask import Flask, jsonify, request
import os
import time
from image_proc import ImageProcess
import json
import redis
import datetime
import threading

RECV_FOLDER='FileRecv'
global possibility

app = Flask(__name__)

@app.route('/')
def index():
    return 'Hello,welcome to the edge computing server!'


@app.route('/device/get_info', methods=['POST'])
def get_info():
    global possibility
    msg_data=request.json
    print("收到消息：",msg_data)
    return jsonify(possibility)

@app.route('/device/send_info', methods=['POST'])
def send_info():  
    global possibility
    msg_data=request.json
    print("收到消息：",msg_data)
    possibility=msg_data['content']
    return jsonify('已成功收到消息！')

@app.route('/device/send_image', methods=['POST'])
def process_image():
    global possibility
    """parse file data"""
    image_file = request.files['content']
    file_path=os.path.join(app.root_path,RECV_FOLDER,image_file.filename)
    image_file.save(file_path)
    file_size = os.stat(file_path).st_size
    results,time=ImageProcess(file_path)
    print('file size: {0:.0f} KB'.format(file_size/1024))
    return jsonify({'proc_results':results,'proc_time':time})

if __name__ == '__main__':
    possibility="Hello, this is the initial value of possibility"
    app.run(debug=True,host='0.0.0.0',port=5000)
    
        