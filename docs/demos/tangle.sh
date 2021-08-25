#!/bin/sh

sed -n '/^``` python/,/^```/ p' < "$1" | sed 's/^```.*//g' > "$2"
