#!/usr/bin/env python
#coding=utf8
import re
import urllib
import simplejson
import mimetypes
from tornado import escape
import Cookie

def _render_cookie_back(self):
        return ''.join(['%s=%s;' %(x, morsel.value)
                        for (x, morsel)
                        in self.cookies.items()])
        
def _update_cookies(self, headers):
        try:
            sc = headers['Set-Cookie']
            cookies = escape.native_str(sc)
            while True:
                self.cookies.update(Cookie.SimpleCookie(cookies))
                if cookies.find(',') == -1:
                    break
                cookies = cookies[cookies.find(',') + len(',') :]
        except KeyError:
            return
        
def encode_multipart_formdata(fields, files):
    """
    file = open('uploadfile.dat', 'rb')
    
    self.client.post('/query', { 'a': '1', 'b': '2', 'upload': file })
    
    fields = []
    files = []
    for key, value in data.items():
        if isinstance(value, file):
            files.append([key, value.name, value.read()])
        else:
            fields.append([key, value])
            
    content_type, body = encode_multipart_formdata(fields, files)
    headers = {'Content-Type' : content_type}
    
    
    fields is a sequence of (name, value) elements for regular form fields.
    files is a sequence of (name, filename, value) elements for data to be uploaded as files
    Return (content_type, body) ready for httplib.HTTP instance
    """
    BOUNDARY = '----------ThIs_Is_tHe_bouNdaRY_$'
    CRLF = '\r\n'
    L = []
    for (key, value) in fields:
        L.append('--' + BOUNDARY)
        L.append('Content-Disposition: form-data; name="%s"' % key)
        L.append('')
        L.append(value)
    for (key, filename, value) in files:
        L.append('--' + BOUNDARY)
        L.append('Content-Disposition: form-data; name="%s"; filename="%s"' % (key, filename))
        L.append('Content-Type: %s' % get_content_type(filename))
        L.append('')
        L.append(value)
    L.append('--' + BOUNDARY + '--')
    L.append('')
    body = CRLF.join(L)
    content_type = 'multipart/form-data; boundary=%s' % BOUNDARY
    return content_type, body

def get_content_type(filename):
    return mimetypes.guess_type(filename)[0] or 'application/octet-stream'

def setting_from_object(obj):
    setting = dict()
    for key in dir(obj):
        if key.isupper():
            setting[key.lower()] = getattr(obj, key)
    return setting

def find_subclasses(klass, include_self=False):
    accum = []
    for child in klass.__subclasses__():
        accum.extend(find_subclasses(child, True))
    if include_self:
        accum.append(klass)
    return accum

def vmobile(mobile):
    return re.match(r"((13|14|15|18)\d{9}$)|(\w+[@]\w+[.]\w+)", mobile)

def sendmsg(settings, mobile, content):
    url = "%s?accesskey=%s&secretkey=%s&mobile=%s&content=%s" % (settings['sms_gateway'], settings['sms_key'], settings['sms_secret'], mobile, urllib.quote_plus(content))
    result = simplejson.loads(urllib.urlopen(url).read())
    
    if int(result['result']) > 1:
        raise Exception('无法发送')