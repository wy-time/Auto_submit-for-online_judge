#!/bin/bash
DIR=$(dirname `pwd`/$0)
if [ $# -lt 1 ]; then
    echo "输入参数错误"
    exit 1
fi
if [ $1 == 'cf' ]; then
    if [ $# -ne 3 ]; then
        echo "输入参数错误"
        exit 1
    else
        echo "$1 $2 $3" | python3 $DIR/codeforces.py
    fi
else
    echo "功能待完成"
fi
