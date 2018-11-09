from ftplib import  FTP
import os

password = os.environ['USER_PASS']
login= os.environ['USER_NAME']
host = os.environ['USER_HOST']
port = os.environ['USER_PORT']

print(password)
print(login)
print(host)

connection =  FTP(host,login,password)



def uploadThis(path):
    files = os.listdir(path)
    os.chdir(path)
    for f in files:
        if os.path.isfile(path + r'\{}'.format(f)):
            fh = open(f, 'rb')
            connection.storbinary('STOR %s' % f, fh)
            fh.close()
        elif os.path.isdir(path + r'\{}'.format(f)):
            connection.mkd(f)
            connection.cwd(f)
            uploadThis(path + r'\{}'.format(f))
        connection.cwd('..')
    os.chdir('..')
uploadThis('.') # no
