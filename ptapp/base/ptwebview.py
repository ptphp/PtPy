from PySide.QtWebKit import QWebView,QWebInspector,QWebSettings,QWebPage
from .ptwebpage import PtWebPage

from PySide.QtCore import SIGNAL
from PySide.QtGui import QFont

csstext = """
  body {
    background-color: #058;
    margin: 0px;
    color: red;
  }
  """

class PtWebView(QWebView):
    def __init__(self, parent=None, userData=None,inspector = True):
        QWebView.__init__(self, parent)  

        settings = QWebSettings.globalSettings()
        settings.setFontFamily(QWebSettings.StandardFont, 'Helvetica')
        settings.setFontSize(QWebSettings.DefaultFontSize, 12)

        self.webpage = page = PtWebPage(self)        
        self.setPage(page) 
        self.connect(self, SIGNAL('loadFinished(bool)'), self.onLoadFinished)
        self.settings().setAttribute(
                    QWebSettings.WebAttribute.DeveloperExtrasEnabled, True)
        #path = os.getcwd()
        #self.settings().setUserStyleSheetUrl(QUrl.fromLocalFile(path + "/myCustom.css"))

        font = QFont("Helvetica")
        font.setPixelSize(12)
        self.setFont(font)
        # or globally:
        # QWebSettings.globalSettings().setAttribute(
        #     QWebSettings.WebAttribute.DeveloperExtrasEnabled, True)
        if inspector:
            self.inspector = QWebInspector()
            self.inspector.setPage(self.page())
            self.inspector.hide()

        self.page().setLinkDelegationPolicy(QWebPage.DelegateAllLinks)
        self.page().linkClicked.connect(self._on_page_link_clicked)
        
    def _on_page_link_clicked(self,url):
        self.load(url)
        
    def onLoadFinished(self, ok):
        print ok

