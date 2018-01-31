import socket

route_ip="127.0.0.1"
route_port=9999

client=socket.socket(family=socket.AF_INET,type=socket.SOCK_STREAM)
client.connect((route_ip,route_port))
client.send(b'hello')
response = client.recv(2048)
print(response)