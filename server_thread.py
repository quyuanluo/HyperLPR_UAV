import socket
import os
import sys
import json
import time
from PIL import Image
import HyperLPRLite as pr
from cv2 import cv2
import numpy as np
import threading

RECV_FOLDER='FileRecv'
ADDRESS=('10.0.0.214',8000)

g_socket_server=None #负责监听的socket
g_conn_pool = []  # 连接池

def init():
    """
    初始化服务端
    绑定端口
    启用监听
    """
    global g_socket_server
    g_socket_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  
    #g_socket_server.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
    g_socket_server.bind(ADDRESS)
    g_socket_server.listen(5)  # 最大等待数（有很多人理解为最大连接数，其实是错误的）
    print("[Server] start，wait for client connecting...")

def accept_client():
    """
    接收新连接
    """
    global g_conn_pool
    while True:
        connection, addr = g_socket_server.accept()  # 阻塞，等待客户端连接
        print('[Server] accept new connection from ', addr)
        g_conn_pool.append(connection) # 将新的连接加入到连接池里面
        thread = threading.Thread(target=user_thread, args=(connection, addr)) # 给每个客户端创建一个独立的线程进行管理
        thread.setDaemon(True) # 设置成守护线程
        thread.start()      # 开始线程

def user_thread(connection, address):
    """
    消息处理
    """
    try:
        feedback={'type': 'feedback',
                'content': 'you have connected to the server!'} 
        connection.sendall(json.dumps(feedback).encode("utf-8"))
    except Exception:
        print('[Server] 反馈问候信息出错！')
    while True:  # 侦听、接收消息
        try:
            obj = json.loads(connection.recv(1024).decode("utf-8"))      

            if obj['type']=='img_req':
                print("[Server] 准备调用图像接收和处理程序！")
                recv_image(connection,obj["img_name"],obj["img_size"],obj['client_name']) # 调用图像接收函数
                proc_results,proc_time=ImageProcessingTest(os.path.join(RECV_FOLDER,obj["client_name"],obj["img_name"])) # 处理图像，获得结果
                print(proc_results,proc_time)
                proc_result_info={'proc_results':proc_results,
                              'proc_time':proc_time}
                feedback={'type':'proc_results',
                            'content':proc_result_info}
                connection.sendall(json.dumps(feedback).encode("utf-8")) # 返回结果
                broadcast(connection,{'type':'broadcast_result','client_name':obj['client_name'],'content':proc_result_info})
            elif obj['type']=='msg_req':
                print('[Server] 收到<{}>的概率消息为{}'.format(obj['client_name'],obj['content']))
                print('[Server] 准备广播概率消息！')
                broadcast(connection,{'type':'broadcast_data','client_name':obj['client_name'],'content':obj['content']})
                feedback={'type': 'feedback',
                        'content': '收到消息，并已广播该消息给其他用户！'} 
                connection.sendall(json.dumps(feedback).encode('utf-8'))
                
        except Exception as e:
            print(e)
            print("[Server] 侦听、接收消息出错！")
            remove_client(connection)
            break

def recv_image(connection,file_name,file_size,client_name):
    print('[Server] 正在接收[{0}]的图像文件[{1}]，大小为[{2} KB]......'.format(client_name,file_name,file_size))
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))     #当前目录
    path = os.path.join(BASE_DIR,RECV_FOLDER,client_name,file_name)
    f = open(path,'wb')
    has_receive=0
    while has_receive!=file_size:
        try:
            recv_data=connection.recv(1024)                       
            f.write(recv_data)
            has_receive+=len(recv_data)
            percent = 1.0 * has_receive *100/ file_size
            sys.stdout.write("\rReceived: {0:.0f}% --- {1:} kB".format(percent,has_receive/1000))
            sys.stdout.flush()
        except Exception as e:
            print(e)
            print("[Server] 接收图像出错!")
            remove_client(connection)     
            break
    f.close()

    # 返回成功接收图片消息
    if has_receive==file_size:
        print('\n[Server] successfully received the image!')
        feedback={'type': 'feedback',
                'content': 'successfuly received the image!'}
        connection.sendall(json.dumps(feedback).encode('utf-8'))

def ImageProcessing(image_path):
    model = pr.LPR("model/cascade.xml", "model/model12.h5", "model/ocr_plate_all_gru.h5")
    grr = cv2.imread(image_path)
    print( "[Server] 神经网络正在处理图片.......")
    
    # 训练结果，为一个列表，其中每一个元素是包括字符串、自信度和车牌位置的列表
    # 如[['9F72E1', 0.6781167685985565, [145.62, 217.5, 104.53178023338317, 39.0]], 
    #    ['苏E9F72E', 0.8783870339393616, [107.66, 215.05, 140.35348415374756,42.9]]]
    proc_results=model.SimpleRecognizePlateByE2E(grr) 
    # 定义一个去掉结果中的位置信息的变量
    proc_results_without_pos=[]
    print( "[Server] 处理结果为：")
    for result in proc_results:
        print("plate_str:",result[0],"plate_confidence:",result[1])
        result.pop() #去掉结果中的位置信息，位于最后
        proc_results_without_pos.append(result)

    print("[Server] 正在计算处理时间......")
    t0 = time.time()
    for x in range(20):
        model.SimpleRecognizePlateByE2E(grr)
    t = (time.time() - t0)/20.0
    print("Image size: " + str(grr.shape[1])+"x"+str(grr.shape[0]) +  " need " + str(round(t*1000,2))+"ms")
    
    return proc_results_without_pos,t
    

def remove_client(connection):
    global g_conn_pool
    connection.close()
    g_conn_pool.remove(connection)
    print('[Server] {} 已断开连接！'.format(connection))


def broadcast(connection,obj):
    """
    广播
    :connection: 该用户连接不需要收到广播
    :obj: 广播内容,格式为：{'client_name': xxx , 'content': yyy }
    """
    global g_conn_pool
    for conn in g_conn_pool:
        if conn !=connection:
                try:
                    conn.sendall(json.dumps(obj).encode('utf-8'))
                    print('[Server] 成功广播给用户<{}>'.format(conn.getsockname()))
                except Exception as e:
                    print(e)
                    print('[Server] 广播给用户<{}>失败！'.format(conn.getpeername()))
                    remove_client(connection)     
                    continue
            

def ImageProcessingTest(image_path):
    return [['测试',0.9]],1


if __name__ == '__main__':
    # model = pr.LPR("model/cascade.xml", "model/model12.h5", "model/ocr_plate_all_gru.h5")
    # 启动服务器，绑定端口，启用监听
    init()
    # 新开一个线程，用于接收新连接
    thread = threading.Thread(target=accept_client)
    thread.setDaemon(True)
    thread.start()
   
    # accept_client()
    
    # 主线程逻辑  
    while True:
        raddr_set=[]
        if len(g_conn_pool)!=0:
            for connc in g_conn_pool:
                c=connc.getpeername() 
                raddr_set.append(c)
        print('number of client:',len(g_conn_pool))
        print('remote address:')
        for i in raddr_set:
            print(i)
        time.sleep(2)




