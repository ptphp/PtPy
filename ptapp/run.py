import sys

from PySide.QtCore import *
from PySide.QtGui import *
from PySide.QtWebKit import *
from PySide.QtNetwork import *
from PySide.QtNetwork import QNetworkProxy
from base.menu import BaseMenu
from base.win import BaseWin

from base.ptwebview import PtWebView

ERROR, WARNING, INFO, DEBUG = range(4)

def _debug(obj, linefeed=True, outfd=sys.stderr, outputencoding="utf8"):
    """Print a debug info line to stream channel"""
    if isinstance(obj, unicode):
        obj = obj.encode(outputencoding)
    strobj = str(obj) + ("\n" if linefeed else "")
    outfd.write(strobj)
    outfd.flush()

class MainWindow(QMainWindow,BaseMenu,BaseWin):
    def __init__(self,debug_level=ERROR,debug_stream = sys.stderr,):
        super(MainWindow, self).__init__()
        self.webview = PtWebView(self)

        self.setCentralWidget(self.webview)
        self.setWindowTitle("PtApp")
        self.resize(400, 300)
        self.createMenu()
        self.debug_level = debug_level
        self.debug_stream = debug_stream
    
    def _debug(self, level, *args):
        if level <= self.debug_level:
            kwargs = dict(outfd=self.debug_stream)
            _debug(*args, **kwargs)
            
if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = MainWindow(debug_level=INFO)
    win.show()   
    win.webview.load("http://v5.ele.me/")
    #win.webview.load("index.html")
    sys.exit(app.exec_())
