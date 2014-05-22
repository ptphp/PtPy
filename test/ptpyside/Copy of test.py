import sys
from PySide.QtCore import *
from PySide.QtGui import *
from PySide.QtWebKit import *
from PySide.QtNetwork import *
from PySide.QtNetwork import QNetworkProxy

        
class Page(QWebPage):
    def __init__(self, parent):
        QWebPage.__init__(self, parent)  
        self.setNetworkAccessManager(NetworkAccessManager(self))
    #def acceptNavigationRequest(self, frame, request, typeRequest):
    #   return True
  
class NetworkReplyData(QObject):
    def __init__(self, parent, url):
        QObject.__init__(self, parent)
        self.url = url
        self.bytesReceived = 0
        self.bytesTotal = 0
        self.finished = False
        self.errorCode = None
        
class LastBrowserState(object):
    """records the last known state browser"""  
    StateNone = 0x0
    StateLoading = 0x1
    StateComplete = 0x2
    StateError = 0x4
    StateHideProgressBar = 0x100  
  
    __slots__ = ('clearProgressBarTimers', 'icon', 'progress', 'state', 'statusMessage', 'title', 'url')
  
    def __init__(self, icon=None, progress=0, statusMessage=None, state=StateNone, title=None, url=None):
        self.clearProgressBarTimers = []        # timers scheduled for hiding progressBar
        self.progress = 0
        self.icon = QIcon() if icon is None else icon
        self.state = state
        self.statusMessage = "" if statusMessage is None else statusMessage
        self.title = "" if title is None else title
        #NOTE: opening a browser in a new tab may take a while to load.
        # self.url() will return '' untill the page is found, so we handle
        # it ourself and keep track of the last known url in self._lastUrl
        # to give feedback to the user on the navbar. downside is we have
        # to reimplement contextMenuEvent() :-(
        self.url = QUrl() if url is None else url
class Browser(QWebView):
    MaxProgress = 100  
    def __init__(self, parent=None, userData=None):
        QWebView.__init__(self, parent)
  
        self.page = page = Page(self)
        
        self.setPage(page)
        
        #NOTE: we store last progress made to set busy cursor accordingly
        self._lastProgress = 0
        self._userData = userData
        self._networkGetReplies = [[], []]      # (QNetworkReplies, urls)
        self._networkReplySignals = (
            ('downloadProgress(qint64, qint64)', self.onNetworkReplyDownloadProgress),
            ('error(QNetworkReply::NetworkError)', self.onNetworkReplyError),
            ('finished()', self.onNetworkReplyFinished),
            )
  
        # connect actions
        self.connect(self, SIGNAL('loadStarted()'), self.onLoadStarted)
        self.connect(self, SIGNAL('loadProgress(int)'), self.onLoadProgress)
        self.connect(self, SIGNAL('loadFinished(bool)'), self.onLoadFinished)
        self.connect(self.pageAction(QWebPage.Stop), SIGNAL('triggered()'), self.onActionStopTriggered)
  
    ################################
    ## methods
    ################################
    #TODO: impl in BrowserWidget
    def lastProgress(self):
        """returns the last progress made by the browser
        @return: (int) last progress
        """
        return self._lastProgress
  
    def networkGetReplies(self):
        return self._networkGetReplies[1]
  
    def networkGetReply(self, indexReply):
        return self._networkGetReplies[1][indexReply]
  
    def setUserData(self, userData):
        self._userData = userData   
  
    def userData(self):
        return self._userData
  
    ################################
    ## overwritten methods
    ################################
    #def createWindow(self, typeWindow):
    #   pass
  
    def load(self, url):
        self._lastProgress = 0
        return QWebView.load(self, url)
  
    def setUrl(self, url):
        return self.load(url)
  
    def setContents(self, *args):
        """sets the contents of the browser without changing its url"""
        self._lastProgress = 0
        return QWebView.setContents(self, *args)
  
    def setHtml(self, *args):
        """sets the contents of the browser without changing its url"""
        self._lastProgress = 0
        return QWebView.setHtm(self, *args)
  
    def setPage(self, page):
        """"""
        self._lastProgress = 0
        self.connect(
                page.networkAccessManager(), 
                SIGNAL('networkRequestCreated(QNetworkReply*)'), 
                self.onNetworkRequestCreated
                )
  
        self.emit(SIGNAL('pageSet(QWebPage*)'), page)
        return QWebView.setPage(self, page)
  
    def mouseMoveEvent(self, event):
        QWebView.mouseMoveEvent(self, event)
        if self._lastProgress < self.MaxProgress:
            self.setCursor(Qt.BusyCursor)
  
    ###############################
    ## event handlers
    ###############################
    def onActionStopTriggered(self):
        # check wich cursor to set cos we may have busy cursor set
        pt = self.mapFromGlobal(self.cursor().pos())        #TODO: self.mapFromGlobal(self.viewPort().cursor().pos()) ??
        frame = self.page().currentFrame()
        hitTest = frame.hitTestContent(pt)
        #if not hitTest.isNull():       #TODO: looks like hitTest.isNull() alwas returns True
        if hitTest.linkUrl().isValid():
            self.setCursor(Qt.PointingHandCursor)
        else:
            self.setCursor(Qt.ArrowCursor)
  
    def onLoadStarted(self):
        self._lastProgress = 0
        self._networkGetReplies = [[], []]
  
    def onLoadProgress(self, n):
        self._lastProgress = n
  
    def onLoadFinished(self, ok):
        if ok:
            self._lastProgress = self.MaxProgress
        print ok
        self.onActionStopTriggered()
  
    def onPageDownloadRequested(self, networkRequest):
        self.emit(SIGNAL('downloadRequested(const QNetworkRequest &)'), networkRequest)
  
    def onNetworkRequestCreated(self, reply):
        if 1 or reply.operation() == QNetworkAccessManager.GetOperation:
            url = QUrl(reply.url())  # copy url, qt nules it on return    
            
            #print url.toString()
            self._networkGetReplies[0].append(reply)
                   
            networkReplyData = NetworkReplyData(self, url)
            self._networkGetReplies[1].append(networkReplyData)
            for signal, handler in self._networkReplySignals:
                self.connect(reply, SIGNAL(signal), handler) 
            self.emit(SIGNAL('networkGetRequestCreated(int, QObject*)'), self._networkGetReplies[0].index(reply), networkReplyData)
  
    def onNetworkReplyDownloadProgress(self, bytesReceived, bytesTotal):
        reply = self.sender()
        i = self._networkGetReplies[0].index(reply)
        networkReplyData = self._networkGetReplies[1][i]
        networkReplyData.bytesReceived = bytesReceived
        networkReplyData.bytesTotal = bytesTotal
        self.emit(SIGNAL('networkReplyProgress(int, QObject*)'), i, networkReplyData)
  
    def onNetworkReplyError(self, errorCode):
        reply = self.sender()
        i = self._networkGetReplies[0].index(reply)
        networkReplyData = self._networkGetReplies[1][i]
        networkReplyData.finished = True
        networkReplyData.errorCode = errorCode
        self.emit(SIGNAL('networkReplyError(int, QObject*)'), i, networkReplyData)
        #for signal, handler in self._networkReplySignals:
        #   self.disconnect(reply, QtCore.SIGNAL(signal), handler)  
  
    def onNetworkReplyFinished(self):
        reply = self.sender()
        
        url = reply.url().toString()
        if ".gif" in url or ".png" in url or ".jpg" in url or ".css" in url or ".js" in url:
            pass
        else:
            pass
        
        if reply.rawHeader("Set-Cookie"):
            print ""
            print "*" * 40
            print url
            print ""
            print reply.rawHeader("Set-Cookie")
            print ""
        #print reply.url()
        i = self._networkGetReplies[0].index(reply)
        networkReplyData = self._networkGetReplies[1][i]
        networkReplyData.finished = True   
        for signal, handler in self._networkReplySignals:
            self.disconnect(reply, SIGNAL(signal), handler)  
        self.emit(SIGNAL('networkReplyFinished(int, QObject*)'), i, networkReplyData)
        
class NetworkAccessManager(QNetworkAccessManager):  
    def __init__(self, parent):
        QNetworkAccessManager.__init__(self, parent)
        proxy = QNetworkProxy()
        proxy.setType(QNetworkProxy.HttpProxy)
        proxy.setHostName("127.0.0.1")
        proxy.setPort(8888)        
        self.setProxy(proxy)
        
    def createRequest(self, operation, request, outgoingData):  
        url = request.url().toString();
        
        if operation == QNetworkAccessManager.GetOperation:            
            if ".gif" in url or ".jpg" in url or ".png" in url:
                pass#request.setUrl(QUrl('forbidden://localhost/'))
            else:
                if ".js" in url:                    
                    pass
                    #print url
                else:
                    pass
                    #print self.cookieJar()
        
        if operation == QNetworkAccessManager.PostOperation:
            print "=================>> cookie request:"
                 
            url = request.url().toString();
            print "="* 60
            print url
            for c in self.cookieJar().cookiesForUrl(request.url()):
                print c.name(),c.value()
        
        reply = QNetworkAccessManager.createRequest(self, operation, request, outgoingData)
        self.emit(SIGNAL('networkRequestCreated(QNetworkReply*)'), reply)
        #print 'createRequest', reply.url()
        #self.connect(reply, QtCore.SIGNAL('downloadProgress(qint64, qint64)'), self.foo)
        
        
        if operation == QNetworkAccessManager.GetOperation:            
            if ".gif" in url or ".jpg" in url or ".png" in url:
                pass#request.setUrl(QUrl('forbidden://localhost/'))
            else:
                if ".js" in url:                    
                    #print url
                    pass
                else:
                    #print reply.rawHeaderList()
                    pass
                    #print self.cookieJar()        
        
        return reply
    
  
    def foo(self, *args):
        print args  
        

if __name__ == "__main__":
    app = QApplication(sys.argv)
    web = Browser()
    print "init"
    web.load(QUrl("http://www.singaporeair.com/"))
    
    web.show()
sys.exit(app.exec_())
