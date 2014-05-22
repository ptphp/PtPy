from PySide.QtNetwork import QNetworkAccessManager
from PySide.QtNetwork import QNetworkProxy
from PySide.QtCore import SIGNAL, QUrl

import urlparse
from ghost.ghost import QNetworkRequest
class PtNetworkAccessManager(QNetworkAccessManager):  
    _url_filter = []
    def __init__(self, parent):
        QNetworkAccessManager.__init__(self, parent)
        self.finished.connect(self._request_ended)
    def _request_ended(self,reply):
        pass
            
    def createRequest(self, operation, request, outgoingData):
        url = request.url().toString()
        for h in request.rawHeaderList():
            pass
            #self._debug(DEBUG, "  %s: %s" % (h, request.rawHeader(h)))
        if self._url_filter:
            if url in self._url_filter:
                #self._debug(INFO, "URL filtered: %s" % url)
                request.setUrl(QUrl("about:blank"))
            else:
                pass
                #self._debug(DEBUG, "URL not filtered: %s" % url)
        #print url
        #if url == "http://v5.ele.me/":
         #request.setRawHeader("Accept-Encoding","")
        
        reply = QNetworkAccessManager.createRequest(self, operation, request, outgoingData)
        #self.emit(SIGNAL('networkRequestCreated(QNetworkReply*)'), reply)
                
        #if html[:6]=='\x1f\x8b\x08\x00\x00\x00':
        #    html=gzip.GzipFile(fileobj=StringIO(html)).read()
        return reply

    def get_proxy(self):
        """Return string containing the current proxy."""
        return self.proxy()

    def set_proxy(self, string_proxy=None):
        """Set proxy:
        url can be in the form:

            - hostname                        (http proxy)
            - hostname:port                   (http proxy)
            - username:password@hostname:port (http proxy)
            - http://username:password@hostname:port
            - socks5://username:password@hostname:port
            - https://username:password@hostname:port
            - httpcaching://username:password@hostname:port
            - ftpcaching://username:password@hostname:port

        """
        if not string_proxy:
            string_proxy = ''
        if string_proxy:
            urlinfo = urlparse.urlparse(string_proxy)
            # default to http proxy if we have a string
            if not urlinfo.scheme:
                string_proxy = "http://%s" % string_proxy
                urlinfo = urlparse.urlparse(string_proxy)
            
            self.proxy_url = string_proxy
            proxy = QNetworkProxy()
            if urlinfo.scheme == 'socks5':
                proxy.setType(QNetworkProxy.Socks5Proxy)
            elif urlinfo.scheme in ['https', 'http']:
                proxy.setType(QNetworkProxy.HttpProxy)
            elif urlinfo.scheme == 'httpcaching':
                proxy.setType(QNetworkProxy.HttpCachingProxy)
            elif urlinfo.scheme == 'ftpcaching':
                proxy.setType(QNetworkProxy.FtpCachingProxy)
            else:
                proxy.setType(QNetworkProxy.NoProxy)
            if urlinfo.hostname != None:
                proxy.setHostName(urlinfo.hostname)
            if urlinfo.port != None:
                proxy.setPort(urlinfo.port)
            if urlinfo.username != None:
                proxy.setUser(urlinfo.username)
            else:
                proxy.setUser('')
            if urlinfo.password != None:
                proxy.setPassword(urlinfo.password)
            else:
                proxy.setPassword('')
            self.setProxy(proxy)
        return self.proxy()