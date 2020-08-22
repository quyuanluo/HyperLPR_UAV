import socket
import time
import threading
 
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock2=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
 
sock.connect(('10.0.0.214', 5550))
sock2.connect(('10.0.0.223', 5550))
sock.send(b'1')
sock2.send(b'1')
print(sock.recv(1024).decode())
print(sock2.recv(1024).decode())
nickName = input('input your nickname: ')
sock.send(nickName.encode())
sock2.send(nickName.encode())
 
def sendThreadFunc(sk):
    while True:
        try:
            myword = input()
            sk.send(myword.encode())
            #print(sock.recv(1024).decode())
        except ConnectionAbortedError:
            print('Server closed this connection!')
        except ConnectionResetError:
            print('Server is closed!')
    
def recvThreadFunc(sk):
    while True:
        try:
            otherword = sk.recv(1024)
            if otherword:
                print(otherword.decode())
            else:
                pass
        except ConnectionAbortedError:
            print('Server closed this connection!')
 
        except ConnectionResetError:
            print('Server is closed!')
 
 
th1 = threading.Thread(target=sendThreadFunc,args=(sock,))
th2 = threading.Thread(target=recvThreadFunc,args=(sock,))
th3 = threading.Thread(target=sendThreadFunc,args=(sock2,))
th4 = threading.Thread(target=recvThreadFunc,args=(sock2,))
threads = [th1, th2,th3, th4]
 
for t in threads :
    t.setDaemon(True)
    t.start()
t.join()