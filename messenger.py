#!/usr/bin/env python3

import sys
import signal
import IPython
from PyQt4 import QtGui

from browser import BrowserWindow

def main():
  app = QtGui.QApplication(sys.argv)

  main_window = BrowserWindow("http://www.facebook.com/desktop/client")
  main_window.show()

  # enable quitting with ctrl-c
  signal.signal(signal.SIGINT, signal.SIG_DFL)
  sys.exit(app.exec_())

if __name__ == "__main__":
  main()
