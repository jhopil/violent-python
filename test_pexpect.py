import pexpect

PROMPT = ['# ', '>>> ', '> ', '\$ ']

def send_command(child, cmd):
    child.sendline(cmd)
    child.expect(PROMPT)
    print(child.before)


def connect(user, host, passwd):
    ssh_newkey = 'Are you sure you want to continue connecting'
    conn_str = 'ssh ' + user + '@' + host
    child = pexpect.spawn(conn_str)
    ret = child.expect([pexpect.TIMEOUT, ssh_newkey, '[P|p]assword:'])

    if ret == 0:
        print('[-] error connecting')
        return
    if ret == 1:
        child.sendline('yes')
        ret = child.expect([pexpect.TIMEOUT, '[P|p]assword:'])
        if ret == 0:
            print('[-] error connecting')
            return
    
    child.sendline(passwd)
    child.expect(PROMPT)
    return child


def main():
    host = 'localhost'
    user = 'root'
    passwd = 'passwd'
    child = connect(user, host, passwd)
    send_command(child, 'ls -l')


if __name__ == '__main__':
    main()
