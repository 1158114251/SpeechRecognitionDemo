# -*- coding: utf-8 -*-

import numpy as np
from datetime import datetime
import time
import urllib, urllib2, pycurl
import base64
import json
import os
import sys
reload(sys)
sys.setdefaultencoding( "utf-8" )
save_count = 0
save_buffer = []
t = 0
sum = 0
time_flag = 0
flag_num = 0
filename = '2.wav'
duihua = '1'
def getHtml(url):
    page = urllib.urlopen(url)
    html = page.read()
    return html
key = '35ff2856b55e4a7f9eeb86e3437e23fe'
api = 'http://www.tuling123.com/openapi/api?key=' + key + '&info='
while(True):
 
    info ="你好"
    request = api   + info
    response = getHtml(request)
    dic_json = json.loads(response)
    a = dic_json['text']
    print type(a)
    unicodestring = a
    # 将Unicode转化为普通Python字符串："encode"
    utf8string = unicodestring.encode("utf-8")
    print type(utf8string)
    print str(a)
    url = "http://tsn.baidu.com/text2audio?tex="+dic_json['text']+"&lan=zh&per=0&pit=1&spd=7&cuid=7519663&ctp=1&tok=25.41bf315625c68b3e947c49b90788532d.315360000.1798261651.282335-9120612"
    os.system('mpg123 "%s"'%(url))
