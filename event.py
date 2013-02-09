from PyQt4 import QtCore

def subscribe(event, callback):
  if event not in _events_map:
    _events_map[event] = []
  _events_map[event].append(callback)

def inform(event, *args, **kwargs):
  def _inform_UIT():
    if event in _events_map:
      for callback in _events_map[event]:
        callback(*args, **kwargs)
  run_on_ui_thread(_inform_UIT)

def run_on_ui_thread(action, *, delay_ms=0):
  _marshall.runuithreadsignal.emit(action, delay_ms)

def _run_on_ui_thread_UIT(action, delay_ms):
  # NB: QTimer cannot be used on non-Qt threads.
  QtCore.QTimer.singleShot(delay_ms, action)

class ThreadMarshaller(QtCore.QObject):
  runuithreadsignal = QtCore.pyqtSignal(object, int)

_marshall = ThreadMarshaller()
_marshall.runuithreadsignal.connect(_run_on_ui_thread_UIT, QtCore.Qt.QueuedConnection)

_events_map = {}
