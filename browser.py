import json
from PyQt4 import QtCore
from PyQt4 import QtWebKit
from PyQt4 import QtNetwork

from external import External
import settings

class BrowserWindow:
  _instances = []

  @staticmethod
  def refresh_all():
    for browser in BrowserWindow._instances:
      browser.refresh()

  def __init__(self, startUrl):
    self._instances.append(self)
    self._startUrl = startUrl
    self._web = QtWebKit.QWebView()
    self.external = External(self)
    frame = self._web.page().mainFrame()
    frame.javaScriptWindowObjectCleared.connect(self._cleared_callback)
    manager = self._web.page().networkAccessManager()
    manager.setCookieJar(SettingsBasedCookieJar())
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
    access_token = settings.get_setting("AccessToken")
    if access_token != "":
      url += "?access_token=" + access_token
    self._web.load(QtCore.QUrl(url))

  def show(self):
    self._web.show()


class SettingsBasedCookieJar(QtNetwork.QNetworkCookieJar):
  def __init__(self):
    QtNetwork.QNetworkCookieJar.__init__(self)
    self._cookies = settings.get_setting("CookieJar", {})

  def setCookiesFromUrl(self, cookieList, url):
    cookiesForHost = self._cookies.get(url.host(), {})
    for cookie in cookieList:
      name = bytes(cookie.name()).decode('utf-8')
      value = bytes(cookie.value()).decode('utf-8')
      cookiesForHost[name] = value
    self._cookies[url.host()] = cookiesForHost
    settings.set_setting("CookieJar", self._cookies)
    return True

  def cookiesForUrl(self, url):
    cookieList = []
    for (name, value) in self._cookies.get(url.host(), {}).items():
      cookieList.append(QtNetwork.QNetworkCookie(name, value))
    return cookieList
