#! /bin/bash

script_dir=`dirname $BASH_SOURCE`

control_file="$script_dir/control"
version=`cat $script_dir/../VERSION`

tmpdir=`mktemp -d`
mkdir "$tmpdir/DEBIAN"
cp "$control_file" "$tmpdir/DEBIAN/control"
sed -i s/'{VERSION}'/"$version"/ "$tmpdir/DEBIAN/control"

(cd "$script_dir/../.."; python3 setup.py install --root="$tmpdir")

fakeroot dpkg-deb --build "$tmpdir" "fbmessenger-$version.deb"
