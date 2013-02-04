from PyQt4 import QtCore
import mosquitto

import settings

rc_map = ["success",
          "unacceptable protocol version",
          "identifier rejected",
          "server unavailable",
          "bad user name or password",
          "not authorized"]

_subscriptions = []
_client = None

_callback_qobj = None
is_connected = False

def connect():
  # TODO(jacko): reconnect when the auth info changes
  url = "orcart.facebook.com"
  port = 443
  global _client
  _client = mosquitto.Mosquitto("linuxmessenger")
  _client.on_connect = _on_connect
  _client.on_disconnect = _on_disconnect
  _client.on_message = _on_message
  _client.username_pw_set(
      settings.get_setting("UserId"),
      settings.get_setting("AccessToken"))
  _client.tls_set("/tmp/test.pem")
  _client.connect_async(url, port)
  _client.loop_start()

def subscribe(topic):
  if topic not in _subscriptions:
    _subscriptions.append(topic)
  if _client:
    _client.subscribe(topic, 0)

# We don't want the callbacks running on the mqtt thread, so we create this
# dummy object with a signal to marshall us onto the UI thread. If we add more
# callbacks, they'll need similar marshalling.
def register_message_callback(callback):
  global _callback_qobj
  if _callback_qobj:
    raise RuntimeError("callback already registered")
  class EventHolder(QtCore.QObject):
    message_received = QtCore.pyqtSignal(str, str)
  _callback_qobj = EventHolder()
  _callback_qobj.message_received.connect(callback)

def _on_connect(mosq, obj, rc):
  if rc == 0: # success
    is_connected = True
    print("MQTT connected successfully")
    for topic in _subscriptions:
      _client.subscribe(topic, 0)
  else:
    is_connected = False
    print("MQTT connection failure:", rc_map[rc])

def _on_disconnect(mosq, obj, rc):
  is_connected = False
  print("MQTT disconnected")

def _on_message(mosq, obj, msg):
  topic = msg.topic
  payload = msg.payload.decode('utf-8')
  if _callback_qobj:
    _callback_qobj.message_received.emit(topic, payload)
