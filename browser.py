import json
from PyQt4 import QtCore
from PyQt4 import QtWebKit

from external import External
import settings

class BrowserWindow:

  def __init__(self, startUrl):
    self._startUrl = startUrl
    self._web = QtWebKit.QWebView()
    self.external = External(self)
    frame = self._web.page().mainFrame()
    frame.javaScriptWindowObjectCleared.connect(self._cleared_callback)
    settings = self._web.page().settings()
    settings.setAttribute(
        QtWebKit.QWebSettings.DeveloperExtrasEnabled, True)
    self._web.resize(200, 600)
    self.refresh()

  def callJSFunction(self, name, *args):
    name_str = json.dumps(name)
    args_str = ",".join(json.dumps(arg) for arg in args)
    script = "window[{0}]({1})".format(name_str, args_str)
    self._web.page().mainFrame().evaluateJavaScript(script)

  def _cleared_callback(self):
    frame = self._web.page().mainFrame()
    frame.addToJavaScriptWindowObject("external", External(self))

  def navigate(self, url):
    self._web.load(QtCore.QUrl(url))

  def refresh(self):
    url = self._startUrl
    if settings.has_access_token():
      url += "?access_token=" + settings.get_access_token()
    self._web.load(QtCore.QUrl(url))

  def show(self):
    self._web.show()
