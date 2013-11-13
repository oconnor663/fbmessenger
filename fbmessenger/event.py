from PyQt5 import QtCore
import threading

def main_thread_only(func):
    def wrapper(*args, **kwargs):
        if threading.current_thread() != _main_thread:
            message = (func.__name__ +
                    " may only be called from the main thread.")
            print("THREAD VIOLATION:", message)
            raise RuntimeError(message)
        return func(*args, **kwargs)
    return wrapper

@main_thread_only
def subscribe(event, callback):
    if event not in _events_map:
        _events_map[event] = []
    _events_map[event].append(callback)

def inform(event, *args, **kwargs):
    def inform_UIT():
        if event in _events_map:
            for callback in _events_map[event]:
                callback(*args, **kwargs)
    run_on_main_thread(inform_UIT)

def run_on_main_thread(action, *, delay_ms=0, repeating=False):
    if delay_ms == 0 and repeating:
        raise ValueError(
            "Repeating with no delay? That's going to hog the CPU.")
    token = StopToken()
    _marshall.runonmainthreadsignal.emit(action, token, delay_ms, repeating)
    return token

def _run_on_main_thread_UIT(action, token, delay_ms, repeating):
    # NB: QTimer cannot be used on non-Qt threads.
    timer = QtCore.QTimer()
    _token_timer_map[token] = timer
    timer.setSingleShot(not repeating)
    timer.setInterval(delay_ms)
    def action_with_cleanup():
        try:
            action()
        finally:
            if token in _token_timer_map and not repeating:
                del _token_timer_map[token]
    timer.timeout.connect(action_with_cleanup)
    timer.start()

class StopToken():
    @main_thread_only
    def stop(self):
        if self in _token_timer_map:
            _token_timer_map[self].stop()
            del _token_timer_map[self]

class ThreadMarshaller(QtCore.QObject):
    runonmainthreadsignal = QtCore.pyqtSignal(object, object, int, bool)

_marshall = ThreadMarshaller()
_marshall.runonmainthreadsignal.connect(
        _run_on_main_thread_UIT, QtCore.Qt.QueuedConnection)
_events_map = {}
_token_timer_map = {}
_main_thread = threading.current_thread()
