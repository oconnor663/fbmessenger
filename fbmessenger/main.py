#!/usr/bin/env python3

# This import must be first.
from . import application

from . import mqtt
from . import windows
from . import external
from . import network

def main():
    application.init()
    network.init()
    mqtt.init()
    windows.init()
    external.init()

    application.main_loop()

if __name__ == "__main__":
    main()
