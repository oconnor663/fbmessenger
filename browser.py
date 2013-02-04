import json
from os import path
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
    self._webkit = QtWebKit.QWebView()
    self.external = External(self)
    frame = self._webkit.page().mainFrame()
    frame.javaScriptWindowObjectCleared.connect(self._cleared_callback)
    manager = self._webkit.page().networkAccessManager()
    manager.setCookieJar(SettingsBasedCookieJar())
    manager.sslErrors.connect(self._handle_ssl_error)
    websettings = self._webkit.page().settings()
    websettings.setAttribute(
        QtWebKit.QWebSettings.DeveloperExtrasEnabled, True)
    websettings.setAttribute(
        QtWebKit.QWebSettings.LocalStorageEnabled, True)
    websettings.setLocalStoragePath(
        path.join(settings.SETTINGS_DIR, "localstorage"))
    self._webkit.resize(200, 600)
    self.refresh()

  def call_js_function(self, name, *args):
    name_str = json.dumps(name)
    args_str = ",".join(json.dumps(arg) for arg in args)
    script = "window[{0}]({1})".format(name_str, args_str)
    self._webkit.page().mainFrame().evaluateJavaScript(script)

  def _cleared_callback(self):
    frame = self._webkit.page().mainFrame()
    frame.addToJavaScriptWindowObject("external", self.external)

  def _handle_ssl_error(self, reply, errors):
    # Ignore SSL errors when we've overridden the default URL
    if settings.get_setting("BaseUrl"):
      reply.ignoreSslErrors()
      if not settings.get_value("AlreadyPrintedSslIgnore"):
        settings.set_value("AlreadyPrintedSslIgnore", True)
        print("Ignoring SSL errors.")
    else:
      print("SSL error!")

  def navigate(self, url):
    self._webkit.load(QtCore.QUrl(url))

  def refresh(self):
    url = self._startUrl
    access_token = settings.get_setting("AccessToken")
    if access_token != "":
      url += "?access_token=" + access_token
    self._webkit.load(QtCore.QUrl(url))

  def show(self):
    self._webkit.show()


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
