import requests
import time
import json

# EDGE_API_URL='http://localhost:5000/weather/api/weathers'
# target_route = EDGE_API_URL+'/device/request_region_rl'
# url_link = 'http://%s:%s%s' % (self.server_ip, self.server_port, target_route)
# ews_param = {'latitude': 42.332940, 'longitude': -83.047840}
# resp = requests.get('http://localhost:5000/weather/api/weathers')
# print("status code %d for GET cmd %s" % (resp.status_code, resp.text))

#while True:
while True:
    #name='3.jpg'
    name=input("input what you want to send >>>>>> ")
    image_path='images_lib/1/'+name
    image_data = open(image_path, 'rb')
    files = {"image_data": image_data,'image_name':name}
    url_link = 'http://10.0.0.214:5000/device/request_image'
    resp = requests.post(url_link, files=files)
    dic_results=resp.content # 响应的是bytes类型
    dic_results=json.loads(dic_results.decode()) #要变成
    print("results:",dic_results['proc_results'])
    print('processing time:', dic_results['proc_time'])
    time.sleep(1) 