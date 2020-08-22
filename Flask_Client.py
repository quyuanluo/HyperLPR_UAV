import requests
import time
import json

CLIENT_NAME='LAPTOP'
IMAGE_FOLDER='images_lib/1/'
EDGE_API_URL='http://10.0.0.120:5000'
ImgProc_URL=EDGE_API_URL+'/device/request_image'
MsgReq_URL=EDGE_API_URL+'/device/request_message'



def send_message(msg):   
    user_info = {'client_name': CLIENT_NAME,'msg_content':msg}  
    headers = {'content-type': 'application/json'}  
    resp_message = requests.post(MsgReq_URL, json=user_info, headers=headers)   
    return resp_message.json()



def send_image(img_name):
    image_path=IMAGE_FOLDER+img_name
    new_name=CLIENT_NAME+'_'+img_name
    files = {"content": (new_name,open(image_path, 'rb'))}
    resp_img = requests.post(ImgProc_URL,files=files)
    # change JSON type to dic type
    return resp_img.json()
    
    

while True:
    sent_msg=[1,2,3,4]
    return_msg=send_message(sent_msg)
    print(return_msg)
    file_name=input("input what you want to send >>>>>> ")
    proc_results=send_image(file_name)
    print("results:",proc_results['proc_results'])
    print('processing time:', proc_results['proc_time'])
    time.sleep(1) 