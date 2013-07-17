#! /usr/bin/python3

from setuptools import setup

setup(
    name="fbmessenger",
    version="0.1.0",
    description="Linux compatible Python reimplementation of "
    "Facebook Messenger for Windows",
    author="Jack O'Connor",
    author_email="oconnor663@gmail.com",
    url="https://github.com/oconnor663/linuxmessenger",
    packages=['fbmessengerlib'],
    package_data={'fbmessengerlib': ['resources/*']},
    data_files=[
      ('share/applications', ['fbmessenger.desktop']),
      ('share/pixmaps', ['fbmessenger.png']),
      ],
    scripts=['fbmessenger'],
    )
