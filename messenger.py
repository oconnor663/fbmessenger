#!/usr/bin/env python3

import sys
import signal
import IPython
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtWebKit import *

def main():
  app = QApplication(sys.argv)

  web = QWebView()
  web.page().settings().setAttribute(
      QWebSettings.DeveloperExtrasEnabled, True)
  web.load(QUrl("https://www.facebook.com/desktop/client"))
  web.resize(200,600)
  web.show()

  # enable quitting with ctrl-c
  signal.signal(signal.SIGINT, signal.SIG_DFL)
  sys.exit(app.exec_())

if __name__=="__main__":
  main()
