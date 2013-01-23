#!/usr/bin/env python3

import sys
import signal
import IPython
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtWebKit import *

app = QApplication(sys.argv)

web = QWebView()
web.load(QUrl("https://www.facebook.com/desktop/client"))
web.resize(200,600)
web.show()

# enable quitting with ctrl-c
signal.signal(signal.SIGINT, signal.SIG_DFL)
sys.exit(app.exec_())
