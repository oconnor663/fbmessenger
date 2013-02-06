import json
from os import path
from PyQt4 import QtCore
from PyQt4 import QtWebKit
from PyQt4 import QtNetwork

import external
import settings
import event

class BrowserWindow:
  _instances = []

  def __init__(self, startUrl):
    self._instances.append(self)
    self._startUrl = startUrl
    self._view = MessengerWebView()
    self.MOVE_EVENT = self._view.MOVE_EVENT
    self.RESIZE_EVENT = self._view.RESIZE_EVENT
    self.CLOSE_EVENT = self._view.CLOSE_EVENT
    self.WHEEL_EVENT = self._view.WHEEL_EVENT
    self.external = external.External(self)
    frame = self._view.page().mainFrame()
    frame.javaScriptWindowObjectCleared.connect(self._cleared_callback)
    event.subscribe(self.CLOSE_EVENT, self._on_close)
    event.subscribe(self.WHEEL_EVENT, self._on_wheel)
    manager = self._view.page().networkAccessManager()
    manager.setCookieJar(SettingsBasedCookieJar())
    manager.sslErrors.connect(self._handle_ssl_error)
    cache = QtNetwork.QNetworkDiskCache()
    cache.setCacheDirectory(
        path.join(settings.SETTINGS_DIR, "cache"))
    manager.setCache(cache)
    websettings = self._view.page().settings()
    websettings.setAttribute(
        QtWebKit.QWebSettings.DeveloperExtrasEnabled, True)
    websettings.setAttribute(
        QtWebKit.QWebSettings.LocalStorageEnabled, True)
    websettings.setLocalStoragePath(
        path.join(settings.SETTINGS_DIR, "localstorage"))
    event.subscribe(settings.AUTH_CHANGED_EVENT, lambda: self.refresh())
    self.refresh()

  def call_js_function(self, name, *args):
    name_str = json.dumps(name)
    args_str = ",".join(json.dumps(arg) for arg in args)
    script = "window[{0}]({1})".format(name_str, args_str)
    self._view.page().mainFrame().evaluateJavaScript(script)

  def _cleared_callback(self):
    frame = self._view.page().mainFrame()
    frame.addToJavaScriptWindowObject("external", self.external)

  def get_position(self):
    g = self._view.geometry()
    return (g.x(), g.y())

  def get_size(self):
    g = self._view.geometry()
    return (g.width(), g.height())

  def _handle_ssl_error(self, reply, errors):
    # Ignore SSL errors when we've overridden the default URL
    if settings.get_setting("BaseUrl"):
      reply.ignoreSslErrors()
      if not settings.get_value("AlreadyPrintedSslIgnore"):
        settings.set_value("AlreadyPrintedSslIgnore", True)
        print("Ignoring SSL errors.")
    else:
      print("SSL error!")

  def hide(self):
    self._view.hide()

  def is_active(self):
    return self._view.isActiveWindow()

  def navigate(self, url):
    self._view.load(QtCore.QUrl(url))

  def _on_close(self):
    self.external.arbiter_inform_local("FbDesktop.windowClosed", None)

  def _on_wheel(self, delta):
    # 120 is the standard wheel delta, but JS works better with 40 for some
    # reason. This is the same adjustment we use on Windows.
    adjusted_delta = delta * 40 / 120
    self.external.arbiter_inform_local("FbDesktop.mouseWheel", adjusted_delta)

  def refresh(self):
    url = self._startUrl
    access_token = settings.get_setting("AccessToken")
    if access_token != "":
      url += "?access_token=" + access_token
    self._view.load(QtCore.QUrl(url))

  def removeframe(self):
    self._view.setWindowFlags(QtCore.Qt.FramelessWindowHint)

  def set_position(self, x, y):
    self._view.move(x, y)

  def set_size(self, width, height):
    self._view.resize(width, height)

  def set_title(self, title):
    self._view.setWindowTitle(title)

  def show(self, bringtofront=True):
    self._view.show()
    if bringtofront:
      self._view.activateWindow()

# The only way to capture events like move and close is to subclass the
# QWebView and override these methods. We do as little as possible here,
# though, for abstraction's sake.
class MessengerWebView(QtWebKit.QWebView):
  def __init__(self):
    QtWebKit.QWebView.__init__(self)
    self.MOVE_EVENT = object()
    self.CLOSE_EVENT = object()
    self.RESIZE_EVENT = object()
    self.WHEEL_EVENT = object()

  def moveEvent(self, event_obj):
    QtWebKit.QWebView.moveEvent(self, event_obj)
    event.inform(self.MOVE_EVENT)

  def resizeEvent(self, event_obj):
    QtWebKit.QWebView.resizeEvent(self, event_obj)
    event.inform(self.RESIZE_EVENT)

  def closeEvent(self, event_obj):
    QtWebKit.QWebView.closeEvent(self, event_obj)
    event.inform(self.CLOSE_EVENT)

  def wheelEvent(self, event_obj):
    QtWebKit.QWebView.wheelEvent(self, event_obj)
    event.inform(self.WHEEL_EVENT, event_obj.delta())

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
