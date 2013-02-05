import os
from os import path
import json

import event

AUTH_CHANGED_EVENT = object()

def set_setting(key, val):
  _settings[key] = val
  _save_settings()

def get_setting(key, default=""):
  return _settings.get(key, default)

def set_value(key, val):
  _values[key] = val

def get_value(key, default=""):
  return _values.get(key, default)

def get_user_info():
  return (get_setting("UserId"), get_setting("AccessToken"))

def set_user_info(userid, token):
  old_uid, old_token = get_user_info()
  if userid != old_uid or token != old_token:
    set_setting("UserId", userid)
    set_setting("AccessToken", token)
    event.inform(AUTH_CHANGED_EVENT)

def _save_settings():
  if not path.exists(SETTINGS_DIR):
    os.mkdir(SETTINGS_DIR)
  with open(_settings_file, "w") as f:
    json.dump(_settings, f, indent=2, sort_keys=True,
              separators=(',', ': '))

def _load_settings():
  global _settings
  if path.exists(_settings_file):
    with open(_settings_file) as f:
      try:
        _settings = json.load(f)
      except Exception as e:
        print("Loading settings failed: ", e)
        _settings = {}

SETTINGS_DIR = path.expanduser("~/.fbmessenger")

_settings_file = path.join(SETTINGS_DIR, "settings.json")

_values = {}
_settings = {}

_load_settings()
