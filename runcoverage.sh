#!/bin/sh

if ! test -f '.codecovrc' ; then
  echo "Need .codecovrc file containing a token."
  echo "Go and get it at https://codecov.io/gh/stagedml/pylightnix/settings" >&2
  exit 1
fi

codecov -t `cat .codecovrc`
