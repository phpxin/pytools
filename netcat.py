# -*- coding: utf-8 -*-
import pcap
import dpkt
import re

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

def main():
    pc=pcap.pcap(name="eth1")                                             # 抓取 eth1
    pc.setfilter('tcp port 80')                                                       # 过滤表达式 tcp port 80
 
    for p_time, p_data in pc:                                                      # 
        #ret = main_pcap(p_time, p_data)
        ret = hortor_pcap(p_time, p_data)
        if ret:
            print ret 
               
def main_pcap(p_time, p_data): # 解码
        out_format = "%s\t%s\t%s\t%s\t%s\tHTTP/%s"
        p = dpkt.ethernet.Ethernet(p_data) # 
        ret = None
        if p.data.__class__.__name__ == 'IP':
            ip_data = p.data
            src_ip = '%d.%d.%d.%d' % tuple(map(ord,list(ip_data.src)))
            dst_ip = '%d.%d.%d.%d' % tuple(map(ord,list(ip_data.dst)))
            if p.data.data.__class__.__name__=='TCP':
                    tcp_data = p.data.data
                    if tcp_data.dport==80:
                        if tcp_data.data:
                            try:
                                h = dpkt.http.Request(tcp_data.data)# http解码
                                pre = "^/.*$"
                                if match(pre, h.uri):  # url 重写
                                    http_headers = h.headers
                                    host = h.headers['host']
                                    url = "http://" + host + h.uri
                                else:
                                    url = h.uri
        
                                # datetime srcip dstip GET /index.htm HTTP/1.1 # 输出日志格式
                                ret = out_format % (p_time, src_ip, dst_ip, h.method, url, h.version)
                            except Exception,e:
                                print e.message
        
        return ret

def hortor_pcap(p_time, p_data): # 解码
        out_format = "%s\t%s\t%s\t%s\t%s\tHTTP/%s"
        p = dpkt.ethernet.Ethernet(p_data) # 
        ret = None
        if p.data.__class__.__name__ == 'IP':
            ip_data = p.data
            src_ip = '%d.%d.%d.%d' % tuple(map(ord,list(ip_data.src)))
            dst_ip = '%d.%d.%d.%d' % tuple(map(ord,list(ip_data.dst)))
            if p.data.data.__class__.__name__=='TCP':
                    tcp_data = p.data.data
                    if tcp_data.dport==80:
                        if tcp_data.data:
                            try:
                                h = dpkt.http.Request(tcp_data.data)# http解码
                                pre = "^/.*$"
                                if match(pre, h.uri):  # url 重写
                                    http_headers = h.headers
                                    host = h.headers['host']
                                    url = "http://" + host + h.uri
                                else:
                                    url = h.uri
        
                                # datetime srcip dstip GET /index.htm HTTP/1.1 # 输出日志格式
                                if host == 'wx.hortor.net' :
                                    ret = out_format % (p_time, src_ip, dst_ip, h.method, url, h.version)
                                if url.startswith("http://wx.hortor.net/gc/game-list") :
                                    print '!!!!!!!!!!!!!!!!!!!!!!'
                                    
                            except Exception,e:
                                print e.message
                    if tcp_data.sport==80:
                        if tcp_data.data:
                            try:
                                h = dpkt.http.Response(tcp_data.data)# http解码
                                pre = "^/.*$"
                                if match(pre, h.uri):  # url 重写
                                    http_headers = h.headers
                                    host = h.headers['host']
                                    url = "http://" + host + h.uri
                                else:
                                    url = h.uri
        
                                # datetime srcip dstip GET /index.htm HTTP/1.1 # 输出日志格式
                                if host == 'wx.hortor.net' :
                                    ret = out_format % (p_time, src_ip, dst_ip, h.method, url, h.version)
                                if url.startswith("http://wx.hortor.net/gc/game-list") :
                                    print '!!!!!!!!!!!!!!!!!!!!!!'
                                    
                            except Exception,e:
                                print e.message
        return ret
 
def match(pre, line):
    p = re.compile(pre)
    m = p.match(line)
    return m


main()