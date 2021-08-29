#!/bin/sh

# Inspiration: https://github.com/earldouglas/codedown
# https://alvinalexander.com/source-code/awk-script-extract-source-code-blocks-markdown-files/
# https://github.com/eclecticiq/rundoc

rm *pipe
mkfifo inp.pipe
mkfifo out.pipe


python -i -c 'print("aaaaaaa")' <inp.pipe >inp.pipe &
# python -i -c 'print("aaaaaaa")' <inp.pipe &
pid=$!
echo "Pid $pid"
trap "kill $pid" EXIT

socat -ddd READLINE PIPE:inp.pipe
echo "Re-running socat"
socat -ddd READLINE PIPE:inp.pipe

# bash





