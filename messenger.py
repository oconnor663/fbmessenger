#!/usr/bin/env python3

# This import must be first.
import application

import mqtt
import windows
import external

def main():
  application.init()
  mqtt.init()
  external.init()
  windows.init()

  application.main_loop()

if __name__ == "__main__":
  main()
