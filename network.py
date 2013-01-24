from PyQt4 import QtNetwork
from PyQt4 import QtCore

_callbacks = {}

def _finished_handler(networkReply):
  replyBytes = bytes(networkReply.readAll())
  replyStr = replyBytes.decode('utf-8')
  try:
    _callbacks[networkReply](replyStr)
  finally:
    del _callbacks[networkReply]

_manager = QtNetwork.QNetworkAccessManager()
_manager.connect(
    _manager, QtCore.SIGNAL("finished(QNetworkReply *)"),
    _finished_handler)

def async_request(url, callback, method, data):
  request = QtNetwork.QNetworkRequest(QtCore.QUrl(url))
  if method.upper() == "GET":
    reply = _manager.get(request)
  elif method.upper() == "POST":
    reply = _manager.post(request, data)
  else:
    raise ValueError("Method must be GET or POST")

  _callbacks[reply] = callback
