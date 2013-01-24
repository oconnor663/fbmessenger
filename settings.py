_settings = {}
_values = {}
_access_token = None
_uid = None

def set_access_token(uid, token):
  global _access_token, _uid
  _access_token = token
  _uid = uid

def get_access_token():
  return _access_token

def has_access_token():
  return _access_token != None

def set_setting(key, val):
  _settings[key] = val

def get_setting(key):
  return _settings.get(key, "")

def set_value(key, val):
  _values[key] = val

def get_value(key):
  return _values.get(key, "")
