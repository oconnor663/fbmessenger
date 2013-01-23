#!/usr/bin/env python3

import sys
import signal
import IPython
from PyQt4 import QtCore
from PyQt4 import QtGui
from PyQt4 import QtWebKit

from external import External

def main():
  app = QtGui.QApplication(sys.argv)

  web = QtWebKit.QWebView()
  web.page().mainFrame().addToJavaScriptWindowObject(
      "external", External())
  web.page().settings().setAttribute(
      QtWebKit.QWebSettings.DeveloperExtrasEnabled, True)
  web.load(QtCore.QUrl(
    "http://www.facebook.com/desktop/client"))
  web.resize(200, 600)
  web.show()

  # enable quitting with ctrl-c
  signal.signal(signal.SIGINT, signal.SIG_DFL)
  sys.exit(app.exec_())

if __name__ == "__main__":
  main()
