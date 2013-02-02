import os
from os import path
import json

def set_setting(key, val):
  _settings[key] = val
  _save_settings()

def get_setting(key, default=""):
  return _settings.get(key, default)

def set_value(key, val):
  _values[key] = val

def get_value(key, default=""):
  return _values.get(key, default)

def _save_settings():
  if not path.exists(_settings_dir):
    os.mkdir(_settings_dir)
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

_settings_dir = path.expanduser("~/.fbmessenger")
_settings_file = path.join(_settings_dir, "settings.json")

_values = {}
_settings = {}

_load_settings()
