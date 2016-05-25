# -*- coding: utf-8 -*-

'''
建立外键关系
citys => countrys
travels => citys
'''

import mysql.connector
import sys

print sys.argv
if len(sys.argv) < 2 :
    print "usage: python table_img_tool.py createall"
    exit()
    pass


config = {
          'user':'root',
          'password':'lixinxin',
          'host':'SpiderDb',
          'database':'qy_spider'
          }


c_list = ['Asialist', 'Europelist', 'Africalist', 'NorthAmericalist', 'SouthAmericalist', 'Oceanialist', 'Antarcticalist']

cnx = mysql.connector.connect(**config)

xcur = cnx.cursor()
xcur.execute("set names utf8")

if sys.argv[1] == 'createall' :

    for _i in c_list :
        
        _sql = "\
        \
        CREATE TABLE `imgs_" + _i.lower() + "` (\
          `id` int(11) NOT NULL AUTO_INCREMENT,\
          `url` text NOT NULL COMMENT '路径',\
          `createtime` int(11) NOT NULL DEFAULT '0' COMMENT '创建时间',\
          `continent` varchar(200) NOT NULL DEFAULT '' COMMENT '所属大洲',\
          `sign` char(32) NOT NULL DEFAULT '' COMMENT '32位url签名',\
          `referer` text NOT NULL COMMENT '来源',\
          `referer_sign` char(32) NOT NULL DEFAULT '' COMMENT '32位来源url签名',\
          `travel_id` int(11) NOT NULL DEFAULT '0' COMMENT '目的地id，对应travels表id',\
          `savepath` varchar(200) NOT NULL DEFAULT '' COMMENT '图片保存位置',\
          PRIMARY KEY (`id`)\
        ) ENGINE=MyISAM DEFAULT CHARSET=utf8 COMMENT='图片表，分表';\
            "
        
        try:
        
            xcur.execute(_sql)
            
        except mysql.connector.errors.ProgrammingError as pe:
            
            print str(pe)
            pass
        
        
        print _i , 'complete '
elif sys.argv[1] == 'deleteall' :
    
    for _i in c_list :
        
        _sql = "drop table `imgs_" + _i.lower() + "`" 
        try:
        
            xcur.execute(_sql)
            
        except mysql.connector.errors.ProgrammingError as pe:
            
            print str(pe)
            pass
        
        
        print _i , 'complete '
else:
    print 'unknown command ' + sys.argv[1]
    
xcur.close()
cnx.close()
