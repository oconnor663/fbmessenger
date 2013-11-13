import webbrowser
import json
import inspect
import time
from PyQt5 import QtCore

from . import network
from . import settings
from . import mqtt
from . import event
from . import windows
from . import application

# methods on the external object with this decorator are exposed to js
def external_decorator(*types, **results):
    qt_decorator = QtCore.pyqtSlot(*types, **results)
    def decorator(function):
        def wrapper(self, *args):
            # Put special stuff here
            return function(self, *args)
        wrapper.__name__ = function.__name__
        return qt_decorator(wrapper)
    return decorator

# prints a message to remind me to implement this function
def fake_external_decorator(*types, **results):
    def _truncate(s):
        maxlen = 50
        if len(s) > maxlen:
            return s[:maxlen-3] + '...'
        else:
            return s
    qt_decorator = QtCore.pyqtSlot(*types, **results)
    def decorator(function):
        def wrapper(self, *args):
            # Put special stuff here
            arg_names = inspect.getargspec(function)[0][1:]
            frame = inspect.currentframe()
            arg_values = inspect.getargvalues(frame)[3]['args']
            args_str = ", ".join(a + "=" + _truncate(repr(b))
                                 for (a, b) in zip(arg_names, arg_values))
            print("FAKE {0}({1})".format(function.__name__, args_str))
            return function(self, *args)
        wrapper.__name__ = function.__name__
        return qt_decorator(wrapper)
    return decorator

def init():
    windows.main_window.bind_external(External(windows.main_window))
    windows.chat_window.bind_external(External(windows.chat_window))
    windows.toast_window.bind_external(External(windows.toast_window))

    ### main window JS events
    def main_window_moved_or_resized():
        # js doesn't listen for a separate resize event
        arbiter_inform_all("FbDesktop.mainWindowMoved", None)
    event.subscribe(windows.main_window.MOVE_EVENT,
                                    main_window_moved_or_resized)
    event.subscribe(windows.main_window.RESIZE_EVENT,
                                    main_window_moved_or_resized)
    def main_window_activated():
        arbiter_inform_all("FbDesktop.mainWindowActivated", None)
    event.subscribe(windows.main_window.ACTIVATE_EVENT, main_window_activated)
    def main_window_deactivated():
        arbiter_inform_all("FbDesktop.mainWindowDeactivated", None)
    event.subscribe(windows.main_window.DEACTIVATE_EVENT,
                    main_window_deactivated)

    ### chat window js events
    def chat_window_activated():
        bump_last_active_time()
        arbiter_inform_all("FbdChat.chatWindowActivated", None)
    event.subscribe(windows.chat_window.ACTIVATE_EVENT, chat_window_activated)

    ### mqtt events
    def mqtt_message_received(topic, payload):
        arbiter_inform_all("FbDesktop.mqtt_" + topic, payload)
    event.subscribe(mqtt.MESSAGE_RECEIVED_EVENT, mqtt_message_received)
    def mqtt_connection_changed(new_value):
        arbiter_inform_all("FbDesktop.mqttConnectionChanged", new_value)
    event.subscribe(mqtt.CONNECTION_CHANGED_EVENT, mqtt_connection_changed)

def arbiter_inform_all(eventname, payload):
    for externalobj in External._instances:
        externalobj.arbiter_inform_local(eventname, payload)

# Detecting user input to determine idleness isn't possible in a portable way.
# We use a number of different events as a substitute for input:
# - chat window activated
# - chat tabs switched (via the 'open_threads' setting)
# - user starts typing (via the '/typing' mqtt topic)
_last_active_time = time.time()
def bump_last_active_time():
    global _last_active_time
    _last_active_time = time.time()

def is_active():
    idle_limit = 5 * 60 # 5 minutes
    return time.time() - _last_active_time < idle_limit

class External(QtCore.QObject):
    _instances = []

    def __init__(self, browserWindow):
        QtCore.QObject.__init__(self)
        self._browserwindow = browserWindow
        self._arbiter_name = None
        self._instances.append(self)

    @external_decorator(str, str)
    def arbiterInformSerialized(self, eventname, payload):
        # The contract here is that JS will serialize a value, and we will
        # deserialize it before we pass it back in. (Recall that passing it
        # back in entails serializing into json but then interpreting that
        # string as a literal, no net change in serialization level.) This is
        # because in some implementations, JS isn't capable of passing out
        # arbitrary objects.

        # Older version of PyQt4 had a bug where, when the JS string passed in
        # contained surrogate pairs (unicode chars that don't fit in a wchar,
        # like these: "𝟘𝟙𝟚𝟛𝟜𝟝𝟞𝟟𝟠𝟡"), those pairs would be parsed correctly into
        # single Python characters, but an extra '\x00' character was appended
        # to the end of the string for each pair. JSON decoding choked on
        # those, so we removed them here. Keeping this around just in case.
        remove_null_hack_payload = payload.strip('\x00')

        deserialized_payload = json.loads(remove_null_hack_payload)
        arbiter_inform_all(eventname, deserialized_payload)

    def arbiter_inform_local(self, eventname, payload):
        if self._arbiter_name:
            self._browserwindow.call_js_function(
                    self._arbiter_name, eventname, payload)

    @external_decorator()
    def captureMouseWheel(self):
        # no-op
        pass

    @external_decorator()
    def clearHeartBeat(self):
        # no-op
        pass

    @fake_external_decorator(str, str, result=int)
    def asyncConfirm(self, message, caption):
        return 0

    @external_decorator(str)
    def debugLog(self, text):
        print(text)

    @external_decorator(result=str)
    def getAccessToken(self):
        uid, token = settings.get_user_info()
        return token

    @external_decorator(str, result=bool)
    def getCapability(self, capabilityName):
        # TODO(jacko): implement ticker flyouts etc.
        return False

    @external_decorator(str, result=str)
    def getSetting(self, key):
        val = settings.get_setting(key)
        return val

    @fake_external_decorator(result=str)
    def getStateBlob(self):
        return ''

    @external_decorator(str, result=str)
    def getValue(self, key):
        val = settings.get_value(key)
        return val

    @fake_external_decorator(result=str)
    def getVersion(self):
        return ''

    @external_decorator(result=bool)
    def hasAccessToken(self):
        uid, token = settings.get_user_info()
        return bool(token)

    @external_decorator()
    def heartBeat(self):
        # no-op
        pass

    @external_decorator()
    def invalidateAccessToken(self):
        settings.set_user_info('', '')

    @external_decorator(result=bool)
    def isIdle(self):
        return not is_active()

    @external_decorator(result=bool)
    def isMqttConnected(self):
        return mqtt.is_connected

    @external_decorator(result=bool)
    def isToastVisible(self):
        return windows.toast_window.is_visible()

    @external_decorator(str, str)
    def logEvent(self, name, payload):
        # no-op
        pass

    @external_decorator(str, str, str)
    def logEvent2(self, category, name, payload):
        # no-op
        pass

    @external_decorator(str)
    def mqttSubscribe(self, topic):
        mqtt.subscribe(topic)

    @external_decorator(str)
    def navigateBrowserToUrl(self, url):
        if not url.startswith("http://") and not url.startswith("https://"):
            url = "http://" + url
        webbrowser.open(url)

    @external_decorator(str)
    def navigateWindowToUrl(self, url):
        self._browserwindow.navigate(url)

    @external_decorator(str, str, str, str)
    def postWebRequest(self, url, callback, method, poststr):
        def _callback(reply):
            self._browserwindow.call_js_function(callback, reply)
        network.AsyncRequest(url, _callback,
                poststr if method.upper() == "POST" else None)

    @external_decorator()
    def recycle(self):
        self._browserwindow.refresh()

    @external_decorator()
    def releaseMouseWheel(self):
        # no-op
        pass

    @external_decorator(str, str)
    def setAccessToken(self, uid, token):
        settings.set_user_info(uid, token)

    @external_decorator(str)
    def setArbiterInformCallback(self, callback):
        self._arbiter_name = callback

    @external_decorator(int)
    def setIcon(self, icon_id):
        # TODO(jacko) do something with this
        pass

    @external_decorator(str, str)
    def setSetting(self, key, value):
        if key == "open_threads":
            # This setting is changed whenever the user opens a new chat tab,
            # or when the chat window is opened from being closed (this doesn't
            # matter, because it's not foregrounded), but not when a new tab is
            # opened in a foregrounded window by receiving a new message, so it
            # works for us as one signal of user activity.
            bump_last_active_time()
        settings.set_setting(key, value)

    @external_decorator(str, str)
    def setValue(self, key, value):
        settings.set_value(key, value)

    @fake_external_decorator()
    def showChatDevTools(self):
        pass

    @fake_external_decorator()
    def showDevTools(self):
        pass

    @fake_external_decorator()
    def showSidebarDevTools(self):
        pass

    @fake_external_decorator()
    def showToastDevTools(self):
        pass

    @fake_external_decorator()
    def showFlyoutDevTools(self):
        pass

    @fake_external_decorator()
    def showDialogDevTools(self):
        pass

    @fake_external_decorator(str, str)
    def showTickerFlyout(self, url, storyYPos):
        pass

    @fake_external_decorator()
    def hideTickerFlyout(self):
        pass

    @fake_external_decorator()
    def showDialog(self):
        pass

    @fake_external_decorator()
    def hideDialog(self):
        pass

    @fake_external_decorator()
    def hideMainWindow(self):
        pass

    @fake_external_decorator(result=bool)
    def isDocked(self):
        return False

    @fake_external_decorator(result=bool)
    def isWindowVisible(self):
        return False

    @fake_external_decorator()
    def showMainWindow(self):
        pass

    @fake_external_decorator()
    def toggleDock(self):
        pass

    @external_decorator()
    def hideChatWindow(self):
        windows.chat_window.hide()

    @external_decorator(result=bool)
    def isChatWindowActive(self):
        return windows.chat_window.is_active()

    @external_decorator()
    def playIncomingMessageSound(self):
        application.play_message_sound()

    @external_decorator(str, str)
    def sendMessage(self, topic, message):
        if topic == '/typing':
            bump_last_active_time()
        mqtt.publish(topic, message)

    @external_decorator(str)
    def setChatWindowTitle(self, title):
        windows.chat_window.set_title(title)

    @external_decorator(bool)
    def showChatWindow(self, bringtofront):
        windows.show_chat_window()
        if bringtofront:
            windows.chat_window.activate()
        else:
            windows.chat_window.alert()

    @external_decorator(int)
    def setToastHeight(self, height):
        windows.toast_window.set_size(windows.TOAST_WIDTH, height)

    @external_decorator()
    def showToast(self):
        windows.show_toast()

    @external_decorator()
    def closeToast(self):
        windows.toast_window.hide()

    @external_decorator()
    def fadeToast(self):
        fade_ms = 2000
        windows.toast_window.fade(fade_ms)

    # The argument to showCustomToast is passed in as an actual JS object,
    # rather than being serialized. (This worked on Mac, and the function
    # wasn't used on Linux.) QVariant is the type that Qt needs to marshall it.
    #
    # JS checks for this function before calling it, so since it's currently a
    # no-op we don't really need to provide it. I'm keeping is here mostly to
    # document the call signature for future me. TODO(jacko): Use this?
    @external_decorator(QtCore.QVariant)
    def showCustomToast(self, blob):
        pass
