import os
from os import path
import json

_settings = {}
_values = {}
_settings_dir = path.expanduser("~/.fbmessenger")
_settings_file = path.join(_settings_dir, "settings.json")

def set_setting(key, val):
  _settings[key] = val
  save()

def get_setting(key, default=""):
  return _settings.get(key, default)

def set_value(key, val):
  _values[key] = val

def get_value(key):
  return _values.get(key, "")

def save():
  if not path.exists(_settings_dir):
    os.mkdir(_settings_dir)
  with open(_settings_file, "w") as f:
    json.dump(_settings, f, indent=2, sort_keys=True,
              separators=(',', ': '))

def load():
  global _settings
  if path.exists(_settings_file):
    with open(_settings_file) as f:
      try:
        _settings = json.load(f)
      except:
        _settings = {}
