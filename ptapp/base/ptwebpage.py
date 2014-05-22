from PySide.QtWebKit import QWebPage
from .ptnetworkaccessmanager import PtNetworkAccessManager
import webbrowser
class PtWebPage(QWebPage):
    def __init__(self, parent):
        QWebPage.__init__(self, parent)  
        manager = PtNetworkAccessManager(self)
        manager.set_proxy("127.0.0.1:8888")
        self.setNetworkAccessManager(manager)

    def acceptNavigationRequest(self, frame, request, type):
        if(type == QWebPage.NavigationTypeLinkClicked):
            if(frame == self.mainFrame()):
                self.view().load(request.url())
            else:
                webbrowser.open(request.url().toString())
                return False
        return QWebPage.acceptNavigationRequest(self, frame, request, type)


    def userAgentForUrl(self, url):
        return "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1750.154 Safari/537.36"

    def javaScriptConsoleMessage(self, message, line, source):
        """Prints client console message in current output stream."""
        super(PtWebPage, self).javaScriptConsoleMessage(message, line,source)
        log_type = "error" if "Error" in message else "info"
        #Logger.log("%s(%d): %s" % (source or '<unknown>', line, message),
        #sender="Frame", level=log_type)
        #print message, line, source