import socket
import os
import sys
import json
import time
import threading

ADDRESS=('10.0.0.214',8000)
CLIENT_NAME='LAPTOP'
SEND_FOLDER='images_lib/2'


def init():
    """
    初始化客户端
    绑定端口
    """
    global sk 
    sk = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #  初始化客户端，并与服务器建立连接
    print(sk)
    sk.connect(ADDRESS)

def receive_message_thread():
    """
        接受消息线程
        """
    while True:
        try:
            obj = json.loads(sk.recv(1024).decode('utf-8'))
            if obj['type']=='feedback':
                print('\n[Server]: {} '.format(obj['content']))
            elif obj['type']=='broadcast_data':
                print('\n[{0}]: {1}'.format(obj['client_name'],obj['content']))
            elif obj['type']=='broadcast_result':
                print('\n[{0}]: 服务器处理结果为<{1}>'.format(obj['client_name'],obj['content']))
            elif obj['type']=='proc_results':
                print('\n[Server]: 处理结果为<{}>'.format(obj['content'])) # 格式为：{'results':[[车牌,概率],...],'time':时间}
        except Exception:
            print('\n[Client] 接收服务器消息出错！')
            break

def send_file(fileName):
    # print('*********send file************\n',threading.current_thread().name+' '+str(time.time()))
    # print("list the threads:", threading.enumerate())
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    path=os.path.join(BASE_DIR,SEND_FOLDER,fileName)
    file_size = os.stat(path).st_size
    file_info={'type':'img_req',
               'img_name':fileName,
               'img_size':file_size,
               'client_name':CLIENT_NAME}
    
    sk.sendall(json.dumps(file_info).encode("utf-8"))                #第一次发送请求，不是具体内容，而是先发送数据信息

    print("[Client] sending file \'"+fileName+"\' with size of "+str(file_size/1000)+" kB")
    
    f = open(path,'rb')
    has_sent=0
    while has_sent!=file_size:
        data = f.read(1024)
        sk.sendall(data)                          #发送真实数据
        has_sent+=len(data)
        percent = 1.0 * has_sent *100/ file_size
        sys.stdout.write("\r[Client] has sent: {0:.0f}% --- {1:} kB".format(percent,has_sent/1000)) # display sending process
        sys.stdout.flush() 
    f.close()
    print("\n[Client] send finished!")
    print("[Client] waiting for the processing results......")

def send_msg(msg):
    # msg是一个字典{"position":[x,y],"value":value}
    # print('*********send msg************\n',threading.current_thread().name)
    # print("list the threads:", threading.enumerate())
    obj={'type':'msg_req',
            'content':msg,
               'client_name':CLIENT_NAME}
    sk.sendall(json.dumps(obj).encode("utf-8"))                #发送请求,并附上具体信息
    print("[Client] has sent the possibility value")

    
if __name__ == '__main__':
    # 启动客户端，绑定端口
    init()
    # 新开一个线程，用于接收信息
    thread = threading.Thread(target=receive_message_thread)
    thread.setDaemon(True)
    thread.start()


    while True:
        #cmd=input('image or msg or exit? >>>: ')
        cmd='image'
        if cmd=="image":
            #file_name=input("input what you want to send >>>>>> ")
            file_name='1.jpg'
            thread = threading.Thread(target=send_file,args=(file_name,)) # 新开一个线程，用于send信息
            thread.setDaemon(True)
            thread.start()
        elif cmd=='msg':
            #msg=input("input what you want to send >>>>>> ")
            msg='Hello world'
            thread = threading.Thread(target=send_msg,args=(msg,)) # 新开一个线程，用于send信息
            thread.setDaemon(True)
            thread.start()
        elif cmd=='exit':
            break
        print('**********main***************\n',threading.current_thread().name+' '+str(time.time()))
        print("number of threads:",threading.active_count())# get the numer of the current active threads
        print("list the threads:", threading.enumerate())
        time.sleep(10)
