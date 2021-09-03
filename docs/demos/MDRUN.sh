#!/bin/sh

# Inspiration: https://github.com/earldouglas/codedown
# https://alvinalexander.com/source-code/awk-script-extract-source-code-blocks-markdown-files/
# https://github.com/eclecticiq/rundoc

chmod -R +w _mdrun && rm -rf _mdrun
rm *pipe
mkfifo inp.pipe
mkfifo out.pipe

# python -u -i -c '
# import os;
# os.open("out.pipe",os.O_WRONLY);
# os.open("inp.pipe",os.O_WRONLY);
# print("Hellow")'

# exit 1

python -u -i -c '
import os;
os.open("inp.pipe",os.O_RDWR);
os.open("out.pipe",os.O_RDWR);
' <inp.pipe >out.pipe 2>&1 &
# python -u -i -c 'print("Fooooo")' \
#   <inp.pipe >out.pipe 2>&1 &
# python -u -i -c 'print("HELLOOO")' <inp.pipe >out.pipe 2>&1 &
# python -i -c 'print("aaaaaaa")' <inp.pipe &
pid=$!
# sleep 999999999 >out.pipe &
# pid2=$!
# sleep 999999999 >inp.pipe &
# pid3=$!

echo "Pid $pid"
trap "kill $pid $pid2 $pid3" EXIT

bash

# echo "HERE"
# exec 3>inp.pipe 4<out.pipe
# echo "THERE"
# socat -dd STDIN!!STDOUT FD:4!!FD:3
# exec 3>&-
# exec 4>&-


# echo "Re-running socat"
# echo "HERE"
# exec 5>inp.pipe 6<out.pipe
# echo "THERE"
# socat -dd STDIN!!STDOUT FD:6!!FD:5




