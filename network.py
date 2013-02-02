from PyQt4 import QtNetwork
from PyQt4 import QtCore
import urllib.request
import urllib.parse as P

import settings

class AsyncRequest(QtCore.QThread):
  _response_received = QtCore.pyqtSignal(str)
  # We have to keep references to each instance,
  # or the ref counter will delete us.
  _instances = set()

  def __init__(self, url, callback=None, poststr=None):
    QtCore.QThread.__init__(self)
    self._instances.add(self)
    self._url = url
    self._postbytes = poststr.encode("utf-8") if poststr else None
    self._response_received.connect(callback)
    self.finished.connect(self._finish)
    self.start()

  def run(self):
    token_url = _add_access_token(self._url)
    response = urllib.request.urlopen(token_url, self._postbytes)
    response_text = response.read().decode("utf-8")
    self._response_received.emit(response_text)

  def _finish(self):
    self._instances.remove(self)

def _add_access_token(url):
  if not settings.get_setting("AccessToken"):
    return url

  scheme, netloc, path, query_string, fragment = P.urlsplit(url)
  query_params = P.parse_qsl(query_string)
  query_params.append(("access_token", settings.get_setting("AccessToken")))
  new_query_string = P.urlencode(query_params)
  return P.urlunsplit((scheme, netloc, path, new_query_string, fragment))
