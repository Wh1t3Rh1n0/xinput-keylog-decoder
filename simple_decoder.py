#!/usr/bin/env python3


import config.cfg_char_list
keymap = config.cfg_char_list.keymap

import config.cfg_mod_list
keymap.update(config.cfg_mod_list.keymap)

import sys
if len(sys.argv) > 1: log_file = sys.argv[1]
else: log_file = 'test-output.log'

f = open(log_file)
log_data = [line.strip() for line in f.readlines()]
f.close()

for line in log_data:
    key_num = int(line.split(" ")[-1])
    if keymap.get(key_num):
        print(line.replace(str(key_num), keymap.get(key_num)))
    else:
        print(line)