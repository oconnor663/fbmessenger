#! /bin/bash

set -ex

cd `dirname $0`
mkdir fbmessenger-git
cp PKGBUILD fbmessenger-git
tar cfz fbmessenger-git.tar.gz fbmessenger-git
