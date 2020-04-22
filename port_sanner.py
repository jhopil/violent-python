import socket
import os
import sys
import optparse
from threading import Thread, Semaphore
import nmap

screenLock = Semaphore(value=1)
def conn_scan(host, port):
    try:
        conn_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        conn_socket.connect((host, port))

        #conn_socket.send('violent python\r\n')
        #results = conn_socket.recv(100)
        screenLock.acquire()
        print('[+] ' + str(port) + '/tcp open')
    except:
        screenLock.acquire()
        print('[-] ' + str(port) + '/tcp close')
    finally:
        screenLock.release()
        conn_socket.close()                


def port_scan(host, ports):
    try:
        ip = socket.gethostbyname(host)
    except:
        print('[-] cannot resolve ' + host + ': unknown host')
        return

    try:
        name = socket.gethostbyaddr(ip)
        print('\n[+] scan results for: ' + name[0])
    except:
        print('\n[+] scan results for: ' + ip)

    socket.setdefaulttimeout(1)
    for port in ports:
        #print('scanning port ' + port)
        #conn_scan(host, int(port))

        #thread
        t = Thread(target=conn_scan, args=(host, int(port)))
        t.start()


def nmap_scan(host, port):
    scanner = nmap.PortScanner()
    scanner.scan(host, port)
    state = scanner[host]['tcp'][int(port)]['state']
    print(f'[*] {host} tcp/{port} {state}')


def main():
    parser = optparse.OptionParser("usage %prog -H <target host> -p <target port>")
    parser.add_option('-H', dest='host', type='string', help='specify target host')
    parser.add_option('-p', dest='port', type='string', help='specify target port')

    (options, args) = parser.parse_args()
    host = options.host
    ports = options.port #str(options.port).split(',')

    if (host == None) | (ports == None):
        print(parser.usage)
        exit(0)

    #port_scan(host, ports)
    nmap_scan(host, ports)

if __name__ == '__main__':
    main()


    

