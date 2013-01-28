from PyQt4 import QtNetwork
from PyQt4 import QtCore
import urllib.parse as U

import settings

_callbacks = {}

def async_request(url, callback, method, data):
  url_plus_token = _add_access_token(url)
  request = QtNetwork.QNetworkRequest(QtCore.QUrl(url_plus_token))
  if method.upper() == "GET":
    reply = _manager.get(request)
  elif method.upper() == "POST":
    request.setHeader(QtNetwork.QNetworkRequest.ContentTypeHeader,
                      "x-www-form-urlencoded")
    reply = _manager.post(request, data)
  else:
    raise ValueError("Method must be GET or POST")

  _callbacks[reply] = callback

def _finished_handler(networkReply):
  replyBytes = bytes(networkReply.readAll())
  replyStr = replyBytes.decode('utf-8')
  try:
    _callbacks[networkReply](replyStr)
  finally:
    del _callbacks[networkReply]

_manager = QtNetwork.QNetworkAccessManager()
_manager.finished.connect(_finished_handler)

def _add_access_token(url):
  if not settings.get_setting("AccessToken"):
    return url

  scheme, netloc, path, query_string, fragment = U.urlsplit(url)
  query_params = U.parse_qsl(query_string)
  query_params.append(("access_token", settings.get_setting("AccessToken")))
  new_query_string = U.urlencode(query_params)
  return U.urlunsplit((scheme, netloc, path, new_query_string, fragment))
