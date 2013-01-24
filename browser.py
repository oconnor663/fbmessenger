from PyQt4 import QtCore
from PyQt4 import QtWebKit

from external import External

class BrowserWindow:

  def __init__(self, startUrl):
    self.web = QtWebKit.QWebView()
    self.web.page().mainFrame().addToJavaScriptWindowObject(
        "external", External(self))
    self.web.page().settings().setAttribute(
        QtWebKit.QWebSettings.DeveloperExtrasEnabled, True)
    self.web.load(QtCore.QUrl(startUrl))
    self.web.resize(200, 600)

  def callJSFunction(self, name, *args):
    self.web.page().mainFrame().evaluateJavaScript(
        "document.body.innerHTML='foo'")

  def show(self):
    self.web.show()
