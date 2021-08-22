#!/bin/sh

set -ex

FN=$(basename $1)
FS=$(cd "$(dirname $1)"; echo "$(pwd)/$FN")
test -f "$FS"
echo "$FS" | grep '.pdf$'

VER=$(basename $2)
test -n "$VER"

FT=Pylightnix-$(basename $FS .pdf)-$(echo $VER | sed 's/\(.*dev\).*/\1/g;').pdf
FL=Pylightnix-$(basename $FS .pdf)-latest.pdf

CWD=`pwd`
rm -rf /tmp/pylightnix_publish || true
mkdir /tmp/pylightnix_publish
cd /tmp/pylightnix_publish

git clone https://github.com/stagedml/pylightnix-docs
cd pylightnix-docs
rm "$FT" || true
cp "$FS" "$FT"
rm "$FL" || true
cp "$FT" "$FL"
git add "$FT"
git add "$FL"
git commit -m "Add $FT" || true
git push
