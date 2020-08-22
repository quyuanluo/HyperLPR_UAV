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

def SpeedTest(image_path):
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
    
class Server:
    """
    服务器类
    """
    def __init__(self):
        """
        构造
        """
        try:
            self.__socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            print(self.__socket)
        except socket.error as msg:
            print (msg)
            sys.exit(1)
        self._address=ADDRESS
        self.__connections = list()
        self.__nicknames = list()

    def start(self):
        """
        启动服务器
        """
        try:
            # 绑定端口
            self.__socket.bind(self._address)
            # 启用监听
            self.__socket.listen(10)
            print ('[Server] Waiting connection...')
        except socket.error as msg:
            print (msg)
            sys.exit(1)

        # 清空连接
        self.__connections.clear()
        self.__nicknames.clear()
        self.__connections.append(None)
        self.__nicknames.append('System')

        # 开始侦听
        while True:
            connection, address = self.__socket.accept()
            print('[Server] accept new connection from ', address)
            connection.sendall(json.dumps("[Server] Hi, welcome to the server!").encode("utf-8"))

            # 尝试接受数据
            try:
                data = connection.recv(1024).decode("utf-8")       #第一次接收从客户端发过来的信息。第一次获取请求
                data=json.loads(data)
                filename=data["file_name"]
                filesize=data["file_size"]           #第一次提取请求信息，获取  name size 

                self.__connections.append(connection)
                self.__nicknames.append(address)
                    
                if data['file_type']=='image':
                    # 单线程的方式
                    self.__recv_image(len(self.__connections) - 1, filename, filesize)
            
            except Exception:
                print('[Server] 无法接受数据:', connection.getsockname(), connection.fileno())
  

    def __recv_image(self, user_id,filename,filesize):
        """
        接收文件
        """
        connection = self.__connections[user_id]
        nickname = self.__nicknames[user_id]
        
        # 获得当前路径
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))     #当前目录
        path = os.path.join(BASE_DIR,RECV_FOLDER,filename)
        print('[Server] 正在接收图像文件[{0}]，大小为[{1} Bytes]......'.format(filename,filesize))
        f = open(path,'wb')
        has_receive=0
        # 侦听
        while has_receive!=filesize:
            try:
                data=connection.recv(1024)                        #第二次获取请求，这次获取的就是传递的具体内容了，1024为文件发送的单位
                f.write(data)
                has_receive+=len(data)
                percent = 1.0 * has_receive *100/ filesize
                sys.stdout.write("\r[Server] has received: {0:.0f}% --- {1:} kB ".format(percent,has_receive/1000))
                sys.stdout.flush()
            except Exception:
                print('[Server] 连接失效:', connection.getsockname(), connection.fileno())
                self.__connections[user_id].close()
                self.__connections[user_id] = None
                self.__nicknames[user_id] = None
        f.close()


        if has_receive==filesize:
            print('\n[Server] successfully received!')
            connection.sendall(json.dumps('[Server] successfuly received the file!').encode('utf-8'))

            # start processing file, send the processing time to client
            proc_results,proc_time=SpeedTest(os.path.join(RECV_FOLDER,filename))
            proc_result_info={'proc_results':proc_results,
                              'proc_time':proc_time}
            connection.sendall(json.dumps(proc_result_info).encode("utf-8"))
        
        # 处理完关闭当前连接
        # self.__connections[user_id].close()
        # del self.__connections[user_id]
        # del self.__nicknames[user_id]

      
    

if __name__ == '__main__':
    # 打开图像处理模型，并一直开着
    model = pr.LPR("model/cascade.xml", "model/model12.h5", "model/ocr_plate_all_gru.h5")
    server = Server()
    server.start()




