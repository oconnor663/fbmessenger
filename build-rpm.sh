#!/bin/bash

# If you're trying to build an rpm you should probably already have the below setup...but if not....
if [ ! -e /usr/bin/rpmbuild ]; then
    echo -e "ERROR: Please install rpm build tools\nyum install -y rpm-build rpmdevtools"
    exit 1
fi

BUILDROOT=$(dirname $(rpm --eval %{buildroot}))
RPMBUILD_DIR=$(dirname $BUILDROOT)

if [ ! -e "$RPMBUILD_DIR"  ]; then
    # Then you don't have your dev structure setup...so I'll do that for you
    echo "ERROR: You don't have a valid buildroot .  Please run: rpmdev-setuptree"
    exit 1
fi

curl -Lo $RPMBUILD_DIR/SOURCES/master.zip https://github.com/oconnor663/linuxmessenger/archive/master.zip
rpmbuild -ba fbmessenger.spec
