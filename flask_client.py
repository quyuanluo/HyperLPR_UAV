# post get 方法的返回如果用jsonify打包数据，则接收时需要用result.json()
# 将JSON type转化成 dic type


import requests
import time
import json
import threading

NODE_NAME='Laptop'
IMAGE_FOLDER='images_lib/1/'
SERVER_URL={'Laptop':'http://10.0.0.214:5000',
              'EdgeNode14':'http://10.0.0.223:5000',
              'EdgeNode12':'http://10.0.0.70:5000',
              'Raspberry':'http://10.0.0.120:5000'}
send_image_path='/device/send_image'
send_info_path='/device/send_info'
get_info_path='/device/get_info'


def get_info(server_url,msg):
    user_info = {'client_name': NODE_NAME,'content':msg}  
    headers = {'content-type': 'application/json'}  
    result=requests.post(server_url+get_info_path,json=user_info, headers=headers) 
    return result.json()

def send_info(server_url,msg):   
    user_info = {'client_name': NODE_NAME,'content':msg}  
    headers = {'content-type': 'application/json'}  
    result = requests.post(server_url+send_info_path, json=user_info, headers=headers)   
    return result.json()

def send_image(server_url,img_name):
    image_path=IMAGE_FOLDER+img_name
    new_name=NODE_NAME+'_'+img_name
    files = {"content": (new_name,open(image_path, 'rb'))}
    resp_img = requests.post(server_url+send_image_path,files=files)
    return resp_img.json()


    
if __name__ == '__main__':
    while True:
        server_name=input("【System Warning】choose a server: EdgeNode12 or EdgeNode14?>>>>>>")
        #server_name='EdgeNode14'
        server_url=SERVER_URL[server_name]
        msg=input("【System Warning】input the message you want to send >>>>>> ")
        result=send_info(server_url,msg)
        print('【{}】从服务器[{}]获得反馈信息为：{}'.format(NODE_NAME,server_name,result))
        result=get_info(server_url,"get information test")
        print('【{}】从服务器[{}]获得刚才发送的信息为：{}'.format(NODE_NAME,server_name,result))
        file_name=input("【System Warning】input the image name you want to send >>>>>> ")
        proc_results=send_image(server_url,file_name)
        print('【{}】收到服务器[{}]处理结果为：{}'.format(NODE_NAME,server_name,proc_results))