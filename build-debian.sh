#! /bin/bash

script_root=`dirname $0`
cd "$script_root"

control_file="./control-debian"
version=`cat ./VERSION`

mkdir -p debian/DEBIAN
cp $control_file debian/DEBIAN/control
sed -i s/'{VERSION}'/"$version"/ debian/DEBIAN/control

bin_dir="debian/usr/bin"
mkdir -p $bin_dir
cp fbmessenger debian/usr/bin

lib_dir="debian/usr/lib/python3/dist-packages"
mkdir -p $lib_dir
cp -r fbmessengerlib $lib_dir

dpkg-deb --build ./debian "fbmessenger-$version.deb"
