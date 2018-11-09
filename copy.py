from ftplib import  FTP
import os
import  sys


login= sys.argv[1]
password = sys.argv[2]
host = sys.argv[3]


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
