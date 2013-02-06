from PyQt4 import QtCore

def subscribe(event, callback):
  if event not in _events_map:
    _events_map[event] = []
  _events_map[event].append(callback)

def inform(event, *args, **kwargs):
  _marshall.informsignal.emit(event, args, kwargs)

def _inform_UIT(event, args, kwargs):
  if event in _events_map:
    for callback in _events_map[event]:
      callback(*args, **kwargs)

def run_on_ui_thread(action):
  _marshall.runuithreadsignal.emit(action)

def _run_on_ui_thread_UIT(action):
  action()

class ThreadMarshaller(QtCore.QObject):
  informsignal = QtCore.pyqtSignal(object, tuple, dict)
  runuithreadsignal = QtCore.pyqtSignal(object)

_marshall = ThreadMarshaller()
_marshall.informsignal.connect(_inform_UIT, QtCore.Qt.QueuedConnection)
_marshall.runuithreadsignal.connect(_run_on_ui_thread_UIT, QtCore.Qt.QueuedConnection)

_events_map = {}
