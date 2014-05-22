from PySide import QtGui, QtCore, QtWebKit

class Window(QtGui.QWidget):
    def __init__(self):
        QtGui.QWidget.__init__(self)
        self.view = QtWebKit.QWebView(self)
        self.view.settings().setAttribute(
            QtWebKit.QWebSettings.WebAttribute.DeveloperExtrasEnabled, True)
        self.inspector = QtWebKit.QWebInspector(self)
        self.inspector.setPage(self.view.page())
        self.inspector.hide()
        self.splitter = QtGui.QSplitter(self)
        self.splitter.addWidget(self.view)
        self.splitter.addWidget(self.inspector)
        layout = QtGui.QVBoxLayout(self)
        layout.addWidget(self.splitter)
        QtGui.QShortcut(QtGui.QKeySequence('F7'), self,
            self.handleShowInspector)

    def handleShowInspector(self):
        self.inspector.setShown(self.inspector.isHidden())

if __name__ == '__main__':

    import sys
    app = QtGui.QApplication(sys.argv)
    window = Window()
    window.view.load(QtCore.QUrl('http://www.google.com'))
    window.show()
    sys.exit(app.exec_())