import mosquitto

import settings
import event

CONNECTION_CHANGED_EVENT = object()
MESSAGE_RECEIVED_EVENT = object()

rc_map = ["success",
          "unacceptable protocol version",
          "identifier rejected",
          "server unavailable",
          "bad user name or password",
          "not authorized"]

_subscriptions = []
_client = None

is_connected = False

def init():
  # TODO(jacko): reconnect when the auth info changes
  global _client
  _client = mosquitto.Mosquitto("linuxmessenger")
  _client.on_connect = _on_connect
  _client.on_disconnect = _on_disconnect
  _client.on_message = _on_message
  # TODO(jacko): do something reasonable with this certs file
  _client.tls_set("certs.pem")
  event.subscribe(settings.AUTH_CHANGED_EVENT, _reconnect)
  _reconnect()

def subscribe(topic):
  if topic not in _subscriptions:
    _subscriptions.append(topic)
  if _client:
    _client.subscribe(topic, 0)

def _reconnect():
  url = "orcart.facebook.com"
  port = 443
  uid, token = settings.get_user_info()
  _client.username_pw_set(uid, token)
  if is_connected:
    _client.disconnect()
    _client.loop_stop()
  if token:
    _client.connect_async(url, port)
    _client.loop_start()

def _on_connect(mosq, obj, rc):
  global is_connected
  if rc == 0: # success
    _set_is_connected(True)
    for topic in _subscriptions:
      _client.subscribe(topic, 0)
  else:
    _set_is_connected(False)
    # TODO(jacko) put an exponential backoff in here

def _on_disconnect(mosq, obj, rc):
  _set_is_connected(False)

def _on_message(mosq, obj, msg):
  topic = msg.topic
  payload = msg.payload.decode('utf-8')
  event.inform(MESSAGE_RECEIVED_EVENT, topic, payload)

def _set_is_connected(value):
  global is_connected
  if is_connected != value:
    is_connected = value
    event.inform(CONNECTION_CHANGED_EVENT, value)
