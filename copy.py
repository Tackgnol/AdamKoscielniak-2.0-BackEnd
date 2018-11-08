import  pysftp as sftp
import os

password = os.environ['USER_PASS']
login= os.environ['USER_NAME']
host = os.environ['USER_HOST']
port = os.environ['USER_PORT']

print(host)

srv = sftp.Connection(host=host,username=login, password=password, port=port, log=True)



with srv.cd('domains/adamkoscielniak.eu.org/public_python'):
    srv.rmdir('Controllers')
    srv.rmdir('GlobalAPi')
    srv.rmdir('Models')
    srv.rmdir('Utils')
    srv.remove('main.py')
    srv.remove('passenger_wsgi.py')
    srv.mkdir('Controllers')
    srv.put_r('Controllers', 'Controllers' )
    srv.mkdir('GlobalApi')
    srv.put_r('GlobalAPi', 'GlobalAPi')
    srv.mkdir('Models')
    srv.put_r('Models', 'Models')
    srv.mkdir('Utils')
    srv.put_r('Utils', 'Utils')
    srv.put('main.py')
    srv.put('passanger_wsgi.py')
srv.close()