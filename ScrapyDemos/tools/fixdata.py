# -*- coding: utf-8 -*-
import mysql.connector

'''
建立外键关系
citys => countrys
travels => citys
'''

config = {
          'user':'root',
          'password':'lixinxin',
          'host':'SpiderDb',
          'database':'qy_spider'
          }


cnx = mysql.connector.connect(**config)

xcur = cnx.cursor()
xcur.execute("set names utf8")


xcur.execute("select id,url from countrys where id>0 order by id asc") 
result = xcur.fetchall()
for (id,url) in result:
    xcur.execute("update citys set country_id="+('%d' %id)+" where referer like '"+url+"%' or referer='"+url+"'")


xcur.execute("select id,url,en from citys where id>0 order by id asc")
result = xcur.fetchall()
for (id,url,en) in result :
    try:
        xcur.execute("update travels set city_id="+('%d' %id)+",city_en='"+en+"' where referer like '"+url+"%' or referer='"+url+"'") 
        print 'execute '+('%d' %id)+' ok '
    except mysql.connector.errors.ProgrammingError as e:
        print 'error ProgrammingError :'
        print e

xcur.close()
cnx.close()
