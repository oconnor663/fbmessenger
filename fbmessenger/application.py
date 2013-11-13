import sys
import signal
import os.path
from PyQt5 import QtCore
from PyQt5 import QtMultimedia
from PyQt5 import QtWidgets

def init():
    global _app
    _app = QtWidgets.QApplication(sys.argv)
    # Needs to be set for media below
    _app.setApplicationName("fbmessenger")

    # TODO: Does this work on Linux in Qt5?
    global _pling_qsound
    _pling_qsound = QtMultimedia.QSound(resource_path("pling.wav"))

    # Handle Qt's debug output
    QtCore.qInstallMessageHandler(handle_qt_debug_message)

    # Enable quitting with ctrl-c
    signal.signal(signal.SIGINT, signal.SIG_DFL)

def get_qt_application():
    return _app

def handle_qt_debug_message(level, context, message):
    print("Qt debug: {0}:{1}: {2}".format(context.file, context.line, message))

def main_loop():
    sys.exit(_app.exec_())

def resource_path(resource_name):
    this_module = sys.modules[__name__]
    module_dir = os.path.dirname(this_module.__file__)
    return os.path.join(module_dir, "resources", resource_name)

def play_message_sound():
    _pling_qsound.play()

def quit():
    # Don't bother with _app.exit(). Other parts of the app may still use Qt
    # objects while they're being cleaned up, which causes scary errors
    # (https://github.com/oconnor663/fbmessenger/issues/33). Just exit the
    # process directly.
    sys.exit()
