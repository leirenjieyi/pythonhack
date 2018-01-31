import socket

route_ip='172.16.2.140'
route_port=20000

client = socket.socket(family=socket.AF_INET,type=socket.SOCK_DGRAM)
client.sendto(b'hello',(route_ip,route_port))
client.settimeout(2)
(data,addr)=client.recvfrom(2048)
print(data)
