#!/bin/bash

PID=`ps -ef | grep "robot.py" | grep -v grep | awk '{print $2}'`

echo $PID
if [ "$PID" == "" ]; then
    ulimit -c unlimited
    ulimit -v unlimited

    sleep 1

    echo "start run"

    cd /root/TRADER
    python robot.py -d
fi

