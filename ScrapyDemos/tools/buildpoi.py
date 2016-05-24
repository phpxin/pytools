# -*- coding: utf-8 -*-
import mysql.connector

'''

建立POI信息表

'''
from bs4 import BeautifulSoup
from bs4.builder._htmlparser import BeautifulSoupHTMLParser
from types import InstanceType


'''
ht = BeautifulSoup('<div><p class="aaa">aaaaaaaaaaaaaaaa</p></div>','lxml')
_ht = ht.find('p', {'class':'aaa'})
print _ht
ht2 = BeautifulSoup(_ht.string, 'lxml')
print ht2



exit()

'''

def myParse(html):
    
    rdict = {}
    rdict['detail'] = ''

    bsobj = BeautifulSoup(html, 'lxml')
    
    # 详情
    node = bsobj.findAll("div", {"class":"poiDet-detail"})
    if len(node) > 0 :
        rdict['detail'] = node[0].get_text().strip()
        pass
    
    # KV
    kv_nodes = bsobj.find("ul", {"class":"poiDet-tips"}).children
    #print type(kv_nodes)
    #print kv_nodes
    #bs2 = BeautifulSoup(unicode(kv_nodes.string), 'lxml')
    #print bs2
    #lis = kv_nodes.findAll("li")
    #print lis
    for _kv_li in kv_nodes :
        if _kv_li InstanceTy
        '''
        k = _kv_li.find("span", {"class":"title"})
        print k
        v = _kv_li.find("div", {"class":"content"})
        print v
        '''
        print type(_kv_li)

    return rdict


fp = open('../startdemo/travel_htmls/demo.html')
html = fp.read()
#print html
result_dict = myParse(html)
print result_dict
fp.close()

