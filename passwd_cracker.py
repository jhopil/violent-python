import crypt
import hashlib
from base64 import urlsafe_b64encode as encode
from base64 import urlsafe_b64decode as decode

def testpass(cryptpass):
    splits = cryptpass.split('$')
    salt = '$'.join(splits[0:3])
    #print('[*] splits: ' + str(splits) + ', salt: ' + salt)

    dictFile = open('./data/dict.txt', 'r')
    for word in dictFile.readlines():
        word = word.strip('\n')
        cryptword = crypt.crypt(word, salt)
        #print('[*] cryptword: ' + cryptword)
        if(cryptword == cryptpass):
            print('[+] found password: ' + word + '\n')
            return
    print('[-] NOT found password\n')
    

''' for test
def testsha512(cryptPass):
    splits = cryptPass.split('$')
    salt = '$'.join(splits[0:3])

    dictFile = open('dict.txt', 'r')
    for word in dictFile.readlines():
        word = word.strip('\n')
        hash = hashlib.sha512(word.encode('utf-8'))
        hash.update(salt.encode('utf-8'))
        #print('[*] hash: ' + encode(str(hash.digest() + salt)))
        if(hash == cryptPass):
            print('[+] found password: ' + word + '\n')
            return
    print('[-] password not found.\n')
'''


def main():
    passFile = open('./data/pass.txt')
    for line in passFile.readlines():
        if ':' in line:
            user = line.split(':')[0]
            cryptpass = line.split(':')[1].strip(' ')
            print('[*] cracking password for: ' + user)
            testpass(cryptpass)
            #testsha512(cryptPass)

if __name__ == '__main__':
    main()
