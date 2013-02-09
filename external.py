import webbrowser
import json

import network
import settings
import browser
import mqtt
import event
import windows

def arbiter_inform_all(eventname, payload):
  for externalobj in External._instances:
    externalobj.arbiter_inform_local(eventname, payload)

def _on_mqtt_message(topic, payload):
  arbiter_inform_all("FbDesktop.mqtt_" + topic, payload)

def _on_mqtt_change(new_value):
  arbiter_inform_all("FbDesktop.mqttConnectionChanged", new_value)

event.subscribe(mqtt.MESSAGE_RECEIVED_EVENT, _on_mqtt_message)
event.subscribe(mqtt.CONNECTION_CHANGED_EVENT, _on_mqtt_change)

class External(browser.ExternalBase):
  _instances = []

  def __init__(self, browserWindow):
    browser.ExternalBase.__init__(self)
    self._browserwindow = browserWindow
    self._arbiter_name = None
    self._instances.append(self)

  @browser.external_decorator(str, str)
  def arbiterInformSerialized(self, eventname, payload):
    # The contract here is that JS will serialize a value, and we will
    # deserialize it before we pass it back in. (Recall that passing it
    # back in entails serializing into json but then interpreting that
    # string as a literal, no net change in serialization level.) This is
    # because in some implementations, JS isn't capable of passing out
    # arbitrary objects.

    # PyQt4 seems to have a weird bug where, when the JS string passed in
    # contains surrogate pairs (unicode chars that don't fit in a wchar, like
    # these: "𝟘𝟙𝟚𝟛𝟜𝟝𝟞𝟟𝟠𝟡"), those pairs are parsed correctly into single Python
    # characters, but an extra '\x00' character is appended to the end of the
    # string for each pair. JSON decoding chokes on those, so we remove them
    # here.
    # TODO(jacko): Do we need a more general workaround for this issue?
    remove_null_hack_payload = payload.strip('\x00')

    deserialized_payload = json.loads(remove_null_hack_payload)
    arbiter_inform_all(eventname, deserialized_payload)

  def arbiter_inform_local(self, eventname, payload):
    if self._arbiter_name:
      self._browserwindow.call_js_function(
          self._arbiter_name, eventname, payload)

  @browser.external_decorator()
  def captureMouseWheel(self):
    # no-op
    pass

  @browser.external_decorator()
  def clearHeartBeat(self):
    # no-op
    pass

  @browser.fake_external_decorator(str, str, result=int)
  def asyncConfirm(self, message, caption):
    return 0

  @browser.external_decorator(str)
  def debugLog(self, text):
    print(text)

  @browser.external_decorator(result=str)
  def getAccessToken(self):
    uid, token = settings.get_user_info()
    return token

  @browser.external_decorator(str, result=bool)
  def getCapability(self, capabilityName):
    # TODO(jacko): implement ticker flyouts etc.
    return False

  @browser.external_decorator(str, result=str)
  def getSetting(self, key):
    val = settings.get_setting(key)
    return val

  @browser.fake_external_decorator(result=str)
  def getStateBlob(self):
    return ''

  @browser.external_decorator(str, result=str)
  def getValue(self, key):
    val = settings.get_value(key)
    return val

  @browser.fake_external_decorator(result=str)
  def getVersion(self):
    return ''

  @browser.external_decorator(result=bool)
  def hasAccessToken(self):
    uid, token = settings.get_user_info()
    return bool(token)

  @browser.external_decorator()
  def heartBeat(self):
    # no-op
    pass

  @browser.external_decorator()
  def invalidateAccessToken(self):
    settings.set_user_info('', '')

  @browser.fake_external_decorator(result=bool)
  def isIdle(self):
    return False

  @browser.external_decorator(result=bool)
  def isMqttConnected(self):
    return mqtt.is_connected

  @browser.external_decorator(result=bool)
  def isToastVisible(self):
    return windows.toast_window.is_visible()

  @browser.external_decorator(str, str)
  def logEvent(self, name, payload):
    # no-op
    pass

  @browser.external_decorator(str, str, str)
  def logEvent2(self, category, name, payload):
    # no-op
    pass

  @browser.external_decorator(str)
  def mqttSubscribe(self, topic):
    mqtt.subscribe(topic)

  @browser.external_decorator(str)
  def navigateBrowserToUrl(self, url):
    if not url.startswith("http://") and not url.startswith("https://"):
      url = "http://" + url
    webbrowser.open(url)

  @browser.external_decorator(str)
  def navigateWindowToUrl(self, url):
    self._browserwindow.navigate(url)

  @browser.external_decorator(str, str, str, str)
  def postWebRequest(self, url, callback, method, poststr):
    def _callback(reply):
      self._browserwindow.call_js_function(callback, reply)
    network.AsyncRequest(url, _callback,
        poststr if method.upper() == "POST" else None)

  @browser.fake_external_decorator()
  def recycle(self):
    pass

  @browser.external_decorator()
  def releaseMouseWheel(self):
    # no-op
    pass

  @browser.external_decorator(str, str)
  def setAccessToken(self, uid, token):
    settings.set_user_info(uid, token)

  @browser.external_decorator(str)
  def setArbiterInformCallback(self, callback):
    self._arbiter_name = callback

  @browser.external_decorator(int)
  def setIcon(self, icon_id):
    # TODO(jacko) do something with this
    pass

  @browser.external_decorator(str, str)
  def setSetting(self, key, value):
    settings.set_setting(key, value)

  @browser.external_decorator(str, str)
  def setValue(self, key, value):
    settings.set_value(key, value)

  @browser.fake_external_decorator()
  def showChatDevTools(self):
    pass

  @browser.fake_external_decorator()
  def showDevTools(self):
    pass

  @browser.fake_external_decorator()
  def showSidebarDevTools(self):
    pass

  @browser.fake_external_decorator()
  def showToastDevTools(self):
    pass

  @browser.fake_external_decorator()
  def showFlyoutDevTools(self):
    pass

  @browser.fake_external_decorator()
  def showDialogDevTools(self):
    pass

  @browser.fake_external_decorator(str, str)
  def showTickerFlyout(self, url, storyYPos):
    pass

  @browser.fake_external_decorator()
  def hideTickerFlyout(self):
    pass

  @browser.fake_external_decorator()
  def showDialog(self):
    pass

  @browser.fake_external_decorator()
  def hideDialog(self):
    pass

  @browser.fake_external_decorator()
  def hideMainWindow(self):
    pass

  @browser.fake_external_decorator(result=bool)
  def isDocked(self):
    return False

  @browser.fake_external_decorator(result=bool)
  def isWindowVisible(self):
    return False

  @browser.fake_external_decorator()
  def showMainWindow(self):
    pass

  @browser.fake_external_decorator()
  def toggleDock(self):
    pass

  @browser.external_decorator()
  def hideChatWindow(self):
    windows.chat_window.hide()

  @browser.external_decorator(result=bool)
  def isChatWindowActive(self):
    return windows.chat_window.is_active()

  @browser.fake_external_decorator()
  def playIncomingMessageSound(self):
    pass

  @browser.fake_external_decorator(str, str)
  def sendMessage(self, topic, message):
    pass

  @browser.external_decorator(str)
  def setChatWindowTitle(self, title):
    windows.chat_window.set_title(title)

  @browser.external_decorator(bool)
  def showChatWindow(self, bringtofront):
    windows.chat_window.show(bringtofront)

  @browser.external_decorator(int)
  def setToastHeight(self, height):
    windows.toast_window.set_size(330, height)

  @browser.external_decorator()
  def showToast(self):
    windows.show_toast()

  @browser.external_decorator()
  def closeToast(self):
    windows.toast_window.hide()

  @browser.external_decorator()
  def fadeToast(self):
    fade_ms = 2000
    windows.toast_window.fade(fade_ms)
