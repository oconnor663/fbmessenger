import threading

try:
  # python3
  from urllib.request import urlopen
  from urllib.parse import urlsplit, parse_qs, urlencode, urlunsplit
except ImportError:
  #python2
  from urllib import urlopen, urlencode
  from urlparse import urlsplit, parse_qs, urlunsplit

import settings
import event

class AsyncRequest(threading.Thread):
  def __init__(self, url, callback=None, poststr=None):
    threading.Thread.__init__(self)
    self._callback = callback
    self._url = url
    self._postbytes = poststr.encode("utf-8") if poststr else None
    self.start()

  def run(self):
    token_url = add_access_token(self._url)
    response_text = ""
    try:
      response = urlopen(token_url, self._postbytes)
      response_text = response.read().decode("utf-8")
    except Exception as e:
      print("async request failed:", e)
    # avoid a self reference in the callback, so this object can get gc'd
    cached_callback = self._callback
    event.run_on_main_thread(lambda: cached_callback(response_text))

def add_access_token(url):
  uid, token = settings.get_user_info()
  if not token:
    return url
  scheme, netloc, path, query_string, fragment = urlsplit(url)
  query_params = parse_qs(query_string)
  query_params["access_token"] = token
  new_query_string = urlencode(query_params, doseq=True)
  return urlunsplit((scheme, netloc, path, new_query_string, fragment))
