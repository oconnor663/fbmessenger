#! /bin/bash

script_root=`dirname $0`
cd "$script_root"

control_file="./control-debian"
version=`cat ./VERSION`

mkdir -p debian/DEBIAN
cp $control_file debian/DEBIAN/control
sed -i s/'{VERSION}'/"$version"/ debian/DEBIAN/control

python3 setup.py install --root=debian

dpkg-deb --build ./debian "fbmessenger-$version.deb"
