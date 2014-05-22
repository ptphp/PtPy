import sys
from PySide.QtCore import *
from PySide.QtGui import *
from PySide.QtWebKit import *
from PySide.QtNetwork import *
from PySide.QtNetwork import QNetworkProxy
import logging
from ptpy.ptcurl import PtCurl
import pycurl
logger = logging.getLogger('broser')

class Error(Exception):
    """Base class for Ghost exceptions."""
    pass


class TimeoutError(Error):
    """Raised when a request times out"""
    pass

class Logger(logging.Logger):
    @staticmethod
    def log(message, sender="Ghost", level="info"):
        if not hasattr(logger, level):
            raise Error('invalid log level')
        getattr(logger, level)("%s: %s", sender, message)


class Page(QWebPage):
    def __init__(self, parent):
        QWebPage.__init__(self, parent)  
        self.setNetworkAccessManager(NetworkAccessManager(self))
        
    def javaScriptConsoleMessage(self, message, line, source):
        """Prints client console message in current output stream."""
        super(Page, self).javaScriptConsoleMessage(message, line,source)
        log_type = "error" if "Error" in message else "info"
        #Logger.log("%s(%d): %s" % (source or '<unknown>', line, message),
        #sender="Frame", level=log_type)
        print message

class Browser(QWebView):
    def __init__(self, parent=None, userData=None):
        QWebView.__init__(self, parent)  
        self.page = page = Page(self)        
        self.setPage(page) 
        self.connect(self, SIGNAL('loadFinished(bool)'), self.onLoadFinished)
  
    def onLoadFinished(self, ok):
        pass
  
        
class NetworkAccessManager(QNetworkAccessManager):  
    def __init__(self, parent):
        QNetworkAccessManager.__init__(self, parent)
        proxy = QNetworkProxy()
        proxy.setType(QNetworkProxy.HttpProxy)
        proxy.setHostName("127.0.0.1")
        proxy.setPort(8888)        
        self.setProxy(proxy)
        
    def createRequest(self, operation, request, outgoingData):  
        reply = QNetworkAccessManager.createRequest(self, operation, request, outgoingData)
        self.emit(SIGNAL('networkRequestCreated(QNetworkReply*)'), reply)
        return reply
    
class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.browser = Browser()
        self.main_frame = self.browser.page.mainFrame()
        self.setCentralWidget(self.browser)
        self.setWindowTitle("Browser")
        self.resize(400, 300)
        self.createMenu()
        logger.setLevel(logging.INFO)
    def createMenu(self):        
        self.get_cookie_act = QAction("&Get Cookie", self,
                shortcut=QKeySequence.New,
                statusTip="Get Cookie", triggered=self.on_get_cookie)
        
        self.CookieeMenu = self.menuBar().addMenu("&Cookie")
        self.CookieeMenu.addAction(self.get_cookie_act)
        
    def __on_reply_finished(self): 
        content = self.reply.peek(self.reply.bytesAvailable())
        print content
    def on_get_cookie(self):
        man = self.browser.page.networkAccessManager()
      
        element = self.main_frame.findFirstElement("#searchForm")
        url = "http://www.singaporeair.com"+element.attribute("action")
        
        #request = QNetworkRequest()
        #request.setUrl(QUrl(url))
        #request.setRawHeader("User-Agent", "MyOwnBrowser 1.0")
        #request.setRawHeader("Content-Type", "application/x-www-form-urlencoded")
        #reply = man.post(request,"fromHomePage=true&_payByMiles=on&_pwmFlightSearchCheckBox=on&recentSearches=&origin=PEK&destination=BKK&departureDay=23&departureMonth=042014&_tripType=on&returnDay=23&returnMonth=052014&cabinClass=Y&numOfAdults=1&numOfChildren=0&numOfInfants=0&_eventId_flightSearchEvent=&isLoggedInUser=false&numOfChildNominees=&numOfAdultNominees=")
        #reply.finished.connect(self.__on_reply_finished)
        #self.reply = reply
        curl = PtCurl(debug = True,proxy="127.0.0.1:8888")
        data = "fromHomePage=true&_payByMiles=on&_pwmFlightSearchCheckBox=on&recentSearches=&origin=PEK&destination=BKK&departureDay=23&departureMonth=042014&_tripType=on&returnDay=23&returnMonth=052014&cabinClass=Y&numOfAdults=1&numOfChildren=0&numOfInfants=0&_eventId_flightSearchEvent=&isLoggedInUser=false&numOfChildNominees=&numOfAdultNominees="
        
        cookies =[]
        for c in man.cookieJar().allCookies():
            cookies.append(str(c.name())+"="+str(c.value()))
        print self.main_frame.url().toString()
        res = curl.post(url, data,{
                                        pycurl.HTTPHEADER:[
                                                           "Content-Type: application/x-www-form-urlencoded"
                                                           ],
                                        pycurl.COOKIE:";".join(cookies),
                                        pycurl.REFERER:self.main_frame.url().toString(),
                                        pycurl.FOLLOWLOCATION:0
                                        })
        curl.get("http://www.singaporeair.com/booking-flow.form")
        
    def evaluate(self, script):
        """Evaluates script in page frame.

        :param script: The script to evaluate.
        """
        return self.main_frame.evaluateJavaScript("%s" % script)   
if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = MainWindow()
    print "init"
    win.browser.load(QUrl("http://www.singaporeair.com/"))    
    win.show()    
    sys.exit(app.exec_())
