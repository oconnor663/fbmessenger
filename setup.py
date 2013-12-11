#! /usr/bin/python3

import os
from setuptools import setup

with open("packaging/VERSION") as version_file:
    version = version_file.read().strip()

setup(
    name="fbmessenger",
    version=version,
    description="Linux compatible Python reimplementation of "
    "Facebook Messenger for Windows",
    author="Jack O'Connor",
    author_email="oconnor663@gmail.com",
    url="https://github.com/oconnor663/fbmessenger",
    packages=['fbmessenger'],
    package_data={'fbmessenger': ['resources/*']},
    data_files=[
      ('share/applications', ['resources/fbmessenger.desktop']),
      ('share/pixmaps', ['resources/fbmessenger.png']),
      ],
    scripts=['bin/fbmessenger'],
)
