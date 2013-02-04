from PyQt4 import QtCore
import inspect
import webbrowser
import json

import network
import settings
import browser
import mqtt

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

def arbiter_inform_all(eventname, payload):
  for externalobj in External._instances:
    externalobj.arbiter_inform_local(eventname, payload)

def arbiter_inform_mqtt(topic, payload):
  arbiter_inform_all("FbDesktop.mqtt_" + topic, payload)

class External(QtCore.QObject):
  _instances = []

  def __init__(self, browserWindow):
    QtCore.QObject.__init__(self)
    self._browserwindow = browserWindow
    self._arbiter_name = None
    self._instances.append(self)

  @external(str, str)
  def arbiterInformSerialized(self, eventname, payload):
    # The contract here is that JS will serialize a value, and we will
    # deserialize it before we pass it back in. (Recall that passing it
    # back in entails serializing into json but then interpreting that
    # string as a literal, no net change in serialization level.) This is
    # because in some implementations, JS isn't capable of passing out
    # arbitrary objects.
    deserialized_payload = json.loads(payload)
    arbiter_inform_all(eventname, deserialized_payload)

  def arbiter_inform_local(self, eventname, payload):
    if self._arbiter_name:
      self._browserwindow.call_js_function(
          self._arbiter_name, eventname, payload)

  @fake_external()
  def captureMouseWheel(self):
    pass

  @external()
  def clearHeartBeat(self):
    # no-op
    pass

  @fake_external(str, str, result=int)
  def asyncConfirm(self, message, caption):
    return 0

  @external(str)
  def debugLog(self, text):
    print(text)

  @external(result=str)
  def getAccessToken(self):
    token = settings.get_setting("AccessToken")
    return token

  @external(str, result=bool)
  def getCapability(self, capabilityName):
    # TODO(jacko): implement ticker flyouts etc.
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

  @external()
  def heartBeat(self):
    # no-op
    pass

  @external()
  def invalidateAccessToken(self):
    settings.set_setting("AccessToken", "")
    settings.set_setting("UserId", "")
    browser.BrowserWindow.refresh_all()

  @fake_external(result=bool)
  def isIdle(self):
    return False

  @external(result=bool)
  def isMqttConnected(self):
    return mqtt.is_connected

  @fake_external(result=bool)
  def isToastVisible(self):
    return False

  @external(str, str)
  def logEvent(self, name, payload):
    # no-op
    pass

  @external(str, str, str)
  def logEvent2(self, category, name, payload):
    # no-op
    pass

  @external(str)
  def mqttSubscribe(self, topic):
    mqtt.subscribe(topic)

  @external(str)
  def navigateBrowserToUrl(self, url):
    webbrowser.open(url)

  @external(str)
  def navigateWindowToUrl(self, url):
    self._browserwindow.navigate(url)

  @external(str, str, str, str)
  def postWebRequest(self, url, callback, method, poststr):
    def _callback(reply):
      self._browserwindow.call_js_function(callback, reply)
    network.AsyncRequest(url, _callback,
        poststr if method.upper() == "POST" else None)


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
    self._arbiter_name = callback

  @external(int)
  def setIcon(self, icon_id):
    # TODO(jacko) do something with this
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
