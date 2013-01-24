import json
from PyQt4 import QtCore
from PyQt4 import QtWebKit

from external import External

class BrowserWindow:

  def __init__(self, startUrl):
    self._web = QtWebKit.QWebView()
    self.external = External(self)
    frame = self._web.page().mainFrame()
    frame.javaScriptWindowObjectCleared.connect(self._cleared_callback)
    settings = self._web.page().settings()
    settings.setAttribute(
        QtWebKit.QWebSettings.DeveloperExtrasEnabled, True)
    self._web.load(QtCore.QUrl(startUrl))
    self._web.resize(200, 600)

  def callJSFunction(self, name, *args):
    name_str = json.dumps(name)
    args_str = ",".join(json.dumps(arg) for arg in args)
    script = "window[{0}]({1})".format(name_str, args_str)
    self._web.page().mainFrame().evaluateJavaScript(script)

  def _cleared_callback(self):
    frame = self._web.page().mainFrame()
    frame.addToJavaScriptWindowObject("external", External(self))

  def refresh(self):
    self._web.reload()

  def show(self):
    self._web.show()
