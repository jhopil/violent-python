import ftplib

def anon_login(host):
    try:
        ftp = ftplib.FTP(host)
        ftp.login('anonymous', 'me@my.com')
        print(f'[*] {host} FTP anonymous login successed\n')
        ftp.quit()
        return True
    except:
        print(f'[-] {host} FTP anonymous login failed\n')
        return False


def main():
    anon_login('127.0.0.1')
    anon_login('192.168.0.1')


if __name__ == '__main__':
    main()
    