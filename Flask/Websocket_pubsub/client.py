import requests
import json
 
 
def push_msg(msg):
    html = requests.get("http://10.0.0.214:5000/push?msg=%s" % msg)
    print(type(html.text),html.text)
    data=json.loads(html.text)
    print(type(data),data)
 
 
if __name__ == '__main__':
    while True:
        msg = input('>>>>>> please input: ')
        if msg=='exit':
            break
        push_msg(msg)