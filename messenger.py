#!/usr/bin/env python3

import sys
import signal
from PyQt4 import QtGui

from browser import BrowserWindow
import settings

def main():
  app = QtGui.QApplication(sys.argv)

  base_url = "http://www.facebook.com"
  base_url_override = settings.get_setting("BaseUrl")
  if (base_url_override):
    print("BaseUrl:", base_url_override)
    base_url = base_url_override

  main_window = BrowserWindow(base_url + "/desktop/client/")
  main_window.show()

  # enable quitting with ctrl-c
  signal.signal(signal.SIGINT, signal.SIG_DFL)
  sys.exit(app.exec_())

if __name__ == "__main__":
  main()
