# -*- coding: utf-8 -*-
import base64
import random
import os
class ProxyMiddleware(object):
    current_ip_number = 0

    PROXIES = {'ip_port':'', 'user_pass':''}
    def process_request(self, request, spider):
        if os.path.exists("ip.txt") == True:
            f = open("ip.txt", 'r')
            self.PROXIES['ip_port'] = f.readline()
            print self.PROXIES['ip_port']
            f.close()
        proxy = self.PROXIES
        if proxy['user_pass'] is not None:
            request.meta['proxy'] = "http://%s" % proxy['ip_port']
            encoded_user_pass = base64.encodestring(proxy['user_pass'])
            request.headers['Proxy-Authorization'] = 'Basic ' + encoded_user_pass
            # print "ProxyMiddleware have pass" + proxy['ip_port']
        else:
            print "**************ProxyMiddleware no pass************" + proxy['ip_port']
            request.meta['proxy'] = "http://%s" % proxy['ip_port']


