#!/usr/bin/env python3

import sys
import signal
from PyQt4 import QtGui

from browser import BrowserWindow
import settings

def main():
  settings.load()

  app = QtGui.QApplication(sys.argv)

  main_window = BrowserWindow("http://www.facebook.com/desktop/client/")
  main_window.show()

  # enable quitting with ctrl-c
  signal.signal(signal.SIGINT, signal.SIG_DFL)
  sys.exit(app.exec_())

if __name__ == "__main__":
  main()
