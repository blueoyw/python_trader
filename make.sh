#!/bin/bash

python ./make.py
ulimit -c unlimited
#python /root/TRADER/robot.py -d -s 30
python ./robot.py -d -t -k 100000 -s 30
