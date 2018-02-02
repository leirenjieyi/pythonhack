
import sys
import subprocess
import paramiko

def sshcommand(ip,p,user,passwd,command):
    client=paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(ip,port=p,username=user,password=passwd)
    session=client.get_transport().open_session()
    if session.active:
        session.exec_command(command)
        print(session.recv(1024))
    return

def main():
    sshcommand('10.10.10.129',2222,'wayne','123456','ls')

if __name__ == '__main__':
    main()