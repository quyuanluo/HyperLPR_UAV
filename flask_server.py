# 服务端接收请求时，用request.json
# 将传过来的JSON type的数据转化成字典类型
# 根据需要转发的服务名称，修改relay_info函数里面的目标服务器地址
from flask import Flask, jsonify, request
import os
import time
from image_proc import ImageProcess
import json
import redis
import threading
import requests

RECV_FOLDER='FileRecv'
NODE_NAME='Laptop' # 本节点名称
Destination_Node='EdgeNode12' #目的服务器节点名称
SERVER_URL={'Laptop':'http://10.0.0.214:5000',
              'EdgeNode14':'http://10.0.0.223:5000',
              'EdgeNode12':'http://10.0.0.70:5000',
              'Raspberry':'http://10.0.0.120:5000'}
send_image_path='/device/send_image'
send_info_path='/device/send_info'
get_info_path='/device/get_info'




global possibility

app = Flask(__name__)


# 根据需要转发的服务名称，修改relay_info函数里面的目标服务器地址
def relay_info(msg_data):  
    user_info = {'client_name': msg_data['client_name'],'content':msg_data['content'],'relay_server':NODE_NAME}  
    headers = {'content-type': 'application/json'}  
    result=requests.post('http://10.0.0.70:5000/device/send_info', json=user_info, headers=headers)
    return result.json()

@app.route('/')
def index():
    return 'Hello,welcome to the edge computing server!'


@app.route('/device/get_info', methods=['POST'])
def get_info():
    global possibility
    msg_data=request.json
    print(f"【{NODE_NAME}】收到[{msg_data['client_name']}]的消息：{msg_data['content']}")
    return jsonify(possibility)

@app.route('/device/send_info', methods=['POST'])
def send_info():  
    global possibility
    msg_data=request.json
    # 先判断是否为其他服务器转发过来信息
    if 'relay_server' in msg_data:
        print(f"【{NODE_NAME}】收到[{msg_data['relay_server']}]转发自[{msg_data['client_name']}]的消息：{msg_data['content']}")
    else: # 如果不是则转发消息
        print(f"【{NODE_NAME}】收到[{msg_data['client_name']}]的消息：{msg_data['content']}")
        print(f"【{NODE_NAME}】正转发[{msg_data['client_name']}]的消息给[{Destination_Node}]......")
        result=relay_info(msg_data)
        print(f"【{Destination_Node}】{result}")
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
    
        