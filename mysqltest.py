# -*- coding: utf-8 -*-



import mysql.connector
from mysql.connector import connect, Connect
config = {
      'user':'root',
      'password':'lixinxin',
      'host':'localhost',
      'database':'test'
      }

# 创建mysql连接
cnx = mysql.connector.connect(**config)

xcur = cnx.cursor(dictionary=True) 

xcur.execute("set names utf8")

print '1111111111111111111'

xcur.execute("select * from demo where id=1")

info = xcur.fetchone()

if info :
    print info
    for key in xcur.column_names:
        print key , ' = ' , info[key]
else:
    print 'not found'


#xcur.close()
cnx.close()

exit()


'''

10.2.27 MySQLConnection.ping() Method

Syntax:

cnx.ping(attempts=1, delay=0)
Check whether the connection to the MySQL server is still available.

When reconnect is set to True, one or more attempts are made to try to reconnect to the MySQL server using the reconnect() method. Use the delay argument (seconds) if you want to wait between each retry.

When the connection is not available, an InterfaceError is raised. Use the is_connected() method to check the connection without raising an error.

Raises InterfaceError on errors.



isconn = cnx.ping()

print isconn 
'''

isconn = cnx.is_connected()
if isconn :
    print 'connection is ok'
else:
    print 'connection is lose'

# 查询大洲下国家
xcursor = cnx.cursor()
xcursor.execute("select title,content from demo") 
for (title,content) in xcursor:
    print title,content
    pass
xcursor.close()