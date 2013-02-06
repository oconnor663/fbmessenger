#!/usr/bin/env python3

# Python2 defaults to PyQt4's API level 1, but Python3
# defaults to level 2, which is what we want. For
# compatibility, we have to explicitly ask for level 2.
import sip
for module in ("QString", "QUrl"):
  sip.setapi(module, 2)

import sys
import signal
from PyQt4 import QtGui

import settings
import mqtt
import external
import windows

def main():
  app = QtGui.QApplication(sys.argv)

  mqtt.init()
  windows.init(app.desktop())

  # enable quitting with ctrl-c
  signal.signal(signal.SIGINT, signal.SIG_DFL)
  sys.exit(app.exec_())

if __name__ == "__main__":
  main()
