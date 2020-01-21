#!/bin/sh

if ! test -f '.codecovrc' ; then
  echo "Need .codecovrc file containing a codecov token."
  echo "Go and get it at https://codecov.io/gh/stagedml/pylightnix/settings" >&2
  exit 1
fi

if ! which coverage >/dev/null ; then
  echo "coverage not found. Install it with 'sudo -H pip3 install coverage'"
  exit 1
fi

if ! which codecov >/dev/null ; then
  echo "codecov not found. Install it with 'sudo -H pip3 install codecov'"
  exit 1
fi

set -e -x
rm coverage.xml || true
coverage run -m pytest
coverage report -m
codecov -t `cat .codecovrc`
