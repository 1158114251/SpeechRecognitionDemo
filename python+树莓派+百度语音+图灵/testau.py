# -*- coding: utf-8 -*-
from pyaudio import PyAudio, paInt16
import numpy as np
from datetime import datetime
import wave
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
def get_token():
    apiKey = "AxXDYEN27Ks9XHocsGmCEdPm"
    secretKey = "61cd52759f4d704d91c155a22ff7183d"
    auth_url = "https://openapi.baidu.com/oauth/2.0/token?grant_type=client_credentials&client_id=" + apiKey + "&client_secret=" + secretKey;
    res = urllib2.urlopen(auth_url)
    json_data = res.read()
    return json.loads(json_data)['access_token']
def dump_res(buf):
    global duihua
    print "字符串类型"
    print (buf)
    a = eval(buf)
    print type(a)
    if a['err_msg']=='success.':
        #print a['result'][0]#终于搞定了，在这里可以输出，返回的语句
        duihua = a['result'][0]
        print duihua
def use_cloud(token):
    fp = wave.open(filename, 'rb')
    nf = fp.getnframes()
    f_len = nf * 2
    audio_data = fp.readframes(nf)
    cuid = "9120612" #产品id
    srv_url = 'http://vop.baidu.com/server_api' + '?cuid=' + cuid + '&token=' + token
    http_header = [
        'Content-Type: audio/pcm; rate=8000',
        'Content-Length: %d' % f_len
    ]
    c = pycurl.Curl()
    c.setopt(pycurl.URL, str(srv_url)) #curl doesn't support unicode
    #c.setopt(c.RETURNTRANSFER, 1)
    c.setopt(c.HTTPHEADER, http_header)   #must be list, not dict
    c.setopt(c.POST, 1)
    c.setopt(c.CONNECTTIMEOUT, 30)
    c.setopt(c.TIMEOUT, 30)
    c.setopt(c.WRITEFUNCTION, dump_res)
    c.setopt(c.POSTFIELDS, audio_data)
    c.setopt(c.POSTFIELDSIZE, f_len)
    c.perform() #pycurl.perform() has no return val
# 将data中的数据保存到名为filename的WAV文件中
def save_wave_file(filename, data):
    wf = wave.open(filename, 'wb')
    wf.setnchannels(1)
    wf.setsampwidth(2)
    wf.setframerate(SAMPLING_RATE)
    wf.writeframes("".join(data))
    wf.close()
token = get_token()
key = '35ff2856b55e4a7f9eeb86e3437e23fe'
api = 'http://www.tuling123.com/openapi/api?key=' + key + '&info='
while(True):
    os.system('arecord -d 3 -r 8000  -c 1 -t wav -f S16_LE -D plughw:1,0 2.wav')
    use_cloud(token)
    print duihua
    info = duihua
    duihua = ""
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
