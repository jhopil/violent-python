import optparse
from pexpect import pxssh

class Client:
    def __init__(self, host, user, passwd):
        self.host = host
        self.user = user
        self.passwd = passwd
        self.session = self.connect()

    def connect(self):
        try:
            s = pxssh.pxssh()
            s.login(self.host, self.user, self.passwd)
            return s
        except Exception as e:
            print('[-] error connecting: ' + str(e))
            
    def send_command(self, cmd):
        self.session.sendline(cmd)
        self.session.prompt()
        return self.session.before


def botnet_command(command):
    for client in botnet:
        output = client.send_command(command)
        print(f'[*] output from {client.host}')
        print(f'[+] {output}\n')


def add_client(host, user, passwd):
    client = Client(host, user, passwd)
    botnet.append(client)


botnet = []
def main():
    add_client('127.0.0.1', 'root', 'passwd')
    add_client('127.0.0.1', 'root', 'passwd')
    
    botnet_command('uname -v')
    botnet_command('cat /etc/issue')


if __name__ == '__main__':
    main()

