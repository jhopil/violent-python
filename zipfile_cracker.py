import zipfile
import optparse
from threading import Thread

def extract_file(zfile, passwd):
    #zfile = zipfile.ZipFile(zname)
    try:
        zfile.extractall(pwd=passwd.encode())
        print('[+] found passwd: ' + passwd)    
    except:
        pass


def main():
    parser = optparse.OptionParser('usage %prog -f <zipfile> -d <dictionary>')
    parser.add_option('-f', dest='zname', type='string', help='specify zip file')
    parser.add_option('-d', dest='dname', type='string', help='specify dictionary file')
    parser.add_option('-p', dest='pname', type='string', help='specify passwd')

    (options, args) = parser.parse_args()
    if (options.zname == None) | (options.dname == None):
        print(parser.usage)
        exit(0)
    else:
        zname = options.zname
        dname = options.dname
    
    zfile = zipfile.ZipFile(zname)
    dicfile = open(dname)
    for line in dicfile.readlines():
        passwd = line.strip('\n')
        #print('[*] passwd: ' + passwd)
        t = Thread(target=extract_file, args=(zfile, passwd))
        t.start()


if __name__ == '__main__':
    main()
