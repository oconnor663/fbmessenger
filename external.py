from PyQt4 import QtCore
import inspect

import network
import settings
import browser

def external(*types, **results):
  qt_decorator = QtCore.pyqtSlot(*types, **results)
  def decorator(function):
    def wrapper(self, *args):
      # Put special stuff here
      return function(self, *args)
    wrapper.__name__ = function.__name__
    return qt_decorator(wrapper)
  return decorator

def fake_external(*types, **results):
  qt_decorator = QtCore.pyqtSlot(*types, **results)
  def decorator(function):
    def wrapper(self, *args):
      # Put special stuff here
      arg_names = inspect.getargspec(function)[0][1:]
      frame = inspect.currentframe()
      arg_values = inspect.getargvalues(frame)[3]['args']
      args_str = ", ".join(a + "=" + _truncate(repr(b)) for (a, b) in zip(arg_names, arg_values))
      print("FAKE {0}({1})".format(function.__name__, args_str))
      return function(self, *args)
    wrapper.__name__ = function.__name__
    return qt_decorator(wrapper)
  return decorator

def _truncate(s):
  maxlen = 50
  if len(s) > maxlen:
    return s[:maxlen-3] + '...'
  else:
    return s

class External(QtCore.QObject):

  def __init__(self, browserWindow):
    QtCore.QObject.__init__(self)
    self._browserWindow = browserWindow

  @fake_external(str, str)
  def arbiterInformSerialized(self, name, payload):
    pass

  @fake_external()
  def captureMouseWheel(self):
    pass

  @fake_external()
  def clearHeartBeat(self):
    pass

  @fake_external(str, str, result=int)
  def asyncConfirm(self, message, caption):
    return 0

  @fake_external(str)
  def debugLog(self, text):
    pass

  @external(result=str)
  def getAccessToken(self):
    token = settings.get_setting("AccessToken")
    return token

  @fake_external(str, result=bool)
  def getCapability(self, capabilityName):
    return False

  @external(str, result=str)
  def getSetting(self, key):
    val = settings.get_setting(key)
    return val

  @fake_external(result=str)
  def getStateBlob(self):
    return ''

  @external(str, result=str)
  def getValue(self, key):
    val = settings.get_value(key)
    return val

  @fake_external(result=str)
  def getVersion(self):
    return ''

  @external(result=bool)
  def hasAccessToken(self):
    ret = settings.get_setting("AccessToken") != ""
    return ret

  @fake_external()
  def heartBeat(self):
    pass

  @external()
  def invalidateAccessToken(self):
    settings.set_setting("AccessToken", "")
    settings.set_setting("UserId", "")
    browser.BrowserWindow.refresh_all()

  @fake_external(result=bool)
  def isIdle(self):
    return False

  @fake_external(result=bool)
  def isMqttConnected(self):
    return False

  @fake_external(result=bool)
  def isToastVisible(self):
    return False

  @fake_external(str, str)
  def logEvent(self, name, payload):
    pass

  @fake_external(str, str, str)
  def logEvent2(self, category, name, payload):
    pass

  @fake_external(str)
  def mqttSubscribe(self, topic):
    pass

  @fake_external(str)
  def navigateBrowserToUrl(self, url):
    pass

  @external(str)
  def navigateWindowToUrl(self, url):
    self._browserWindow.navigate(url)

  @external(str, str, str, str)
  def postWebRequest(self, url, callback, method, postData):
    def _callback(reply):
      self._browserWindow.callJSFunction(callback, reply)
    network.AsyncRequest(url, _callback,
        postData if method.upper() == "POST" else None)


  @fake_external()
  def recycle(self):
    pass

  @fake_external()
  def releaseMouseWheel(self):
    pass

  @external(str, str)
  def setAccessToken(self, uid, token):
    if token != settings.get_setting("AccessToken"):
      settings.set_setting("AccessToken", token)
      settings.set_setting("UserId", uid)
      browser.BrowserWindow.refresh_all()

  @external(str)
  def setArbiterInformCallback(self, callback):
    settings.set_setting("ArbiterInformCallback", callback)

  @fake_external(int)
  def setIcon(self, icon_id):
    pass

  @external(str, str)
  def setSetting(self, key, value):
    settings.set_setting(key, value)

  @external(str, str)
  def setValue(self, key, value):
    settings.set_value(key, value)

  @fake_external()
  def showChatDevTools(self):
    pass

  @fake_external()
  def showDevTools(self):
    pass

  @fake_external()
  def showSidebarDevTools(self):
    pass

  @fake_external()
  def showToastDevTools(self):
    pass

  @fake_external()
  def showFlyoutDevTools(self):
    pass

  @fake_external()
  def showDialogDevTools(self):
    pass

  @fake_external(str, str)
  def showTickerFlyout(self, url, storyYPos):
    pass

  @fake_external()
  def hideTickerFlyout(self):
    pass

  @fake_external()
  def showDialog(self):
    pass

  @fake_external()
  def hideDialog(self):
    pass
