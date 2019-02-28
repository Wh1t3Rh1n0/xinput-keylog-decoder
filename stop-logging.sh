#!/bin/bash


echo Finding running xinput test commands...
ps aux | grep 'xinput test' | grep -v grep

echo
echo Killing processes...

for PID in $(ps aux | grep 'xinput test' | grep -v grep | awk -F ' ' '{print $2}') ; do
    echo     Killing $PID...
    kill -9 $PID
done

echo
echo Displaying any remaining xinput test commands:
ps aux | grep 'xinput test' | grep -v grep

echo
echo Done.