#! /bin/bash

root=`dirname $BASH_SOURCE`

(cd "$root" && peru sync)

PYTHONPATH="$root" "$root/bin/fbmessenger"
