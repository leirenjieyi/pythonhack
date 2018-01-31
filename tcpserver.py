import socket
import threading

def thread_callback(clientsocket):
    data=clientsocket.recv(1024)
    print(data)
    clientsocket.send(data)
    clientsocket.close()


local_ip='0.0.0.0'
local_port=9999

server=socket.socket(family=socket.AF_INET,type=socket.SOCK_STREAM)
server.bind((local_ip,local_port))
server.listen(5)
print("server listening at %s:%d" % (local_ip,local_port))
while True:
    (client,addr)=server.accept()
    print("accept a client connected from %s:%d" % (addr[0],addr[1]))
    client_thread=threading.Thread(target=thread_callback,args=(client,))
    client_thread.start()

