#!/bin/sh

if ! which pydoc-markdown ; then
  echo "pydoc-markdown not found. Please install it with"
  echo "> sudo -H pip3 install git+https://github.com/stagedml/pydoc-markdown.git@develop"
  exit 1
fi

pydoc-markdown \
  --modules \
    pylightnix.types pylightnix.core pylightnix.stages \
  --search-path  \
    src /usr/lib/python3.6/ > ./docs/Reference.md
