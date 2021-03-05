#!/bin/sh

set -e -x

F=$(basename "$1")
D=$(basename "$1" .tex).pdf
cd -P $(dirname "$1")

rm -rf pythontex-files-* || true
pdflatex --shell-escape -interaction=nonstopmode "$F" || { rm "$D" ; exit 1; }
pythontex "$F"
pdflatex --shell-escape -interaction=nonstopmode "$F" || true
pdflatex --shell-escape -interaction=nonstopmode "$F"
