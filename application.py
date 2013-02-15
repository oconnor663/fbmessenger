# Python2 defaults to PyQt4's API level 1, but Python3
# defaults to level 2, which is what we want. For
# compatibility, we have to explicitly ask for level 2.
import sip
for module in ("QString", "QUrl"):
  sip.setapi(module, 2)

import sys
import signal
from PyQt4 import QtGui

def init():
  global _app
  _app = QtGui.QApplication(sys.argv)

  # enable quitting with ctrl-c
  signal.signal(signal.SIGINT, signal.SIG_DFL)

def main_loop():
  sys.exit(_app.exec_())

def get_desktop_rectangle():
  g = _app.desktop().geometry()
  return (g.x(), g.y(), g.width(), g.height())
