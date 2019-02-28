#!/bin/bash -v

for k in $(xinput | grep -Eio "[a-z].*k.*id=.*slave +keyboard" | grep -vi 'virtual' | grep -iEo 'id=[0-9]+' | cut -d '=' -f 2) ; do
    echo "--- Logging started at $(date +'%Y-%m-%d %H:%M:%S') ---" >> test-output.$k.txt
    nohup xinput test $k >> test-output.$k.txt 2>&1 &
done
