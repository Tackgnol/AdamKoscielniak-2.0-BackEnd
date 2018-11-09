from ftplib import  FTP
import os

password = os.environ['USER_PASS']
login= os.environ['USER_NAME']
host = os.environ['USER_HOST']
port = os.environ['USER_PORT']

connection =  FTP(host,login,password)

def uploadThis(path):
    files = os.listdir(path)
    os.chdir(path)
    for f in files:
        if os.path.isfile(path + r'\{}'.format(f)):
            fh = open(f, 'rb')
            myFTP.storbinary('STOR %s' % f, fh)
            fh.close()
        elif os.path.isdir(path + r'\{}'.format(f)):
            myFTP.mkd(f)
            myFTP.cwd(f)
            uploadThis(path + r'\{}'.format(f))
    myFTP.cwd('..')
    os.chdir('..')
uploadThis('.') # no
