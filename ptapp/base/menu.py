from PySide.QtCore import QObject
from PySide.QtGui import QAction, QKeySequence

class BaseMenu(QObject):        
    def createMenu(self):
        self.get_cookie_act = QAction("&Get Cookie", self,triggered=self.on_get_cookie)
        self.CommonMenu = self.menuBar().addMenu("&Common")
        self.CookieeMenu1 = self.menuBar().addMenu("&Cookie")
        self.CommonMenu.addAction(self.get_cookie_act)
        
    def on_get_cookie(self):
        pass
