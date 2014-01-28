import json
import os
from os import path
import shutil
import traceback

from . import event

AUTH_CHANGED_EVENT = object()

SETTINGS_DIR = path.expanduser("~/.fbmessenger")

_internal_settings_file = path.join(SETTINGS_DIR, "internal_data.json")
_legacy_settings_file = path.join(SETTINGS_DIR, "settings.json")

_user_config_file = path.join(SETTINGS_DIR, "config.py")

_values = {}
_settings = {}
# User settings should not be persisted in the internal data file. That would
# make it hard to unset a setting, because the previous value would stick
# around in internal data. Maintain a separate dictionary containing only those
# settings that were either loaded from disk or set with set_setting(). Only
# the keys in this dictionary will get written back to disk.
_internal_settings = {}

def set_setting(key, val):
    _settings[key] = val
    _internal_settings[key] = val
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
    with open(_internal_settings_file, "w") as f:
        # Only persist internal settings to disk. See comment above.
        json.dump(_internal_settings, f, indent=2, sort_keys=True,
                            separators=(',', ': '))

_default_user_config = '''\
# To configure fbmessenger, set Python variables in this file. For example, to
# make text appear 20% bigger, set the Zoom variable:
#
# Zoom = 1.2
#
# To disable system tray icon, set SystemTray variable to False
SystemTray = True

# This option is only valid if the tray icon is allowed. Set it if you want
# to have the messanger minimized to tray on start:
#
MinimizedOnStart = False
'''

def _read_user_config():
    user_settings = {}

    # If no config file exists, create an empty one with a helpful comment.
    if not path.exists(_user_config_file):
        with open(_user_config_file, "w") as f:
            f.write(_default_user_config)

    # Read the contents of the config file, which should be Python code.
    with open(_user_config_file, "r") as f:
        config_code = f.read()

    # Execute that code and copy the local variables it defines into _settings.
    # If there are exceptions, print them, but continue startup as if the
    # user's config file had been empty.
    try:
        exec(config_code, {}, user_settings)
    except:
        print("Loading {0} failed:".format(_user_config_file))
        traceback.print_exc()
    else:
        _settings.update(user_settings)

def _init():
    if not path.exists(SETTINGS_DIR):
        os.mkdir(SETTINGS_DIR)

    # The settings file used to be called "settings.json". It's been renamed to
    # "internal_data.json" to avoid the impression that users should edit it,
    # but we still need to check for the old path for backwards compatibility.
    # TODO: Eventually remove this legacy code.
    path_to_open = _internal_settings_file
    if not path.exists(path_to_open):
        path_to_open = _legacy_settings_file

    # Read internal settings from disk.
    if path.exists(path_to_open):
        with open(path_to_open) as f:
            try:
                parsed_json = json.load(f)
            except Exception as e:
                print("Loading {0} failed:".format(path_to_open))
                traceback.print_exc()
                # Continuing with startup will overwrite an existing settings
                # file. Save a copy of the bad file for debugging.
                bad_copy_path = path_to_open + ".bad"
                print("Saving the bad file at", bad_copy_path)
                shutil.copyfile(path_to_open, bad_copy_path)
            else:
                _internal_settings.update(parsed_json)
                _settings.update(parsed_json)

    # Reading the user config last allows it to override disk settings.
    _read_user_config()

# Settings like CookieJar are needed at import time, even before application.py
# starts calling init() functions. So we have to read settings from disk as
# soon as this module is imported.
_init()
