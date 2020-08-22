import socket
import os
import sys
import json

SEND_FOLDER='images_lib/1'
ADDRESS=('10.0.0.214',8000)

def send_file(fileName,ADDRESS):
    # 建立Socket连接
    try:
        sk = socket.socket()
        print(sk)
        sk.connect(ADDRESS)
    except socket.error as msg:
        print (msg)
        sys.exit(1)
    # 若连接成功，收到服务器消息
    buffer=sk.recv(1024).decode("utf-8")
    buffer=json.loads(buffer)
    print(buffer)
    # 得到文件绝对路径和文件大小
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    path=os.path.join(BASE_DIR,SEND_FOLDER,fileName)
    file_size = os.stat(path).st_size # 单位是字节
    file_info={'file_type':'image',
               'file_name':fileName,
               'file_size':file_size}
    
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
    print(json.loads(sk.recv(1024).decode('utf-8')))
    print("[Client] waiting for the processing results......")


    proc_result_info=sk.recv(1024).decode('utf-8')
    proc_result_info=json.loads(proc_result_info)

    sk.close() 

    return proc_result_info # return the processing time
    # 返回的是一个字典{'pro_results':结果的列表[["可能车牌1",自信度],["可能车牌2",自信度]],'pro_time':处理时间}



if __name__ == '__main__':
    files=os.listdir(SEND_FOLDER)
    for file_name in files:
        #file_name=input("input what you want to send >>>>>> ")
        proc_result_info=send_file(file_name,ADDRESS)

        print('--- results from server:')
        for result in proc_result_info['proc_results']:
            print(result)

        print('--- processing time: ', proc_result_info['proc_time'])

    
