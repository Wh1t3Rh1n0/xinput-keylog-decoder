#!/usr/bin/env python3

import os
import re
import sys

if len(sys.argv) < 3 or "-h" in sys.argv or "--help" in sys.argv:
    print("""
This script generates key mappings for all the key names listed in
config/key-list.chars.txt and config/key-list.mods.txt.

Run xinput without any arguments to see a list of keyboard devices and device
numbers on your system. This doesn't have to match the device number on the
system you're targeting. It is just used to tell xinput where to read the key
presses used to generate the keymap files.

Usage: %s <keymap type> <local xinput device number>

Valid keymap types:

c   : Character/standalone keys - A, B, 1, 2, <ENTER>, <SPACE>, etc.
m   : Modifiers - <LEFT CTRL>, <RIGHT ALT>, <LEFT SHIFT>, etc.
    """ % sys.argv[0])
    exit()

if sys.argv[1] == "c":
    key_list = "config/key-list.chars.txt"
    output_file = 'config/cfg_char_list.py'
elif sys.argv[1] == "m":
    key_list = "config/key-list.mods.txt"
    output_file = 'config/cfg_mod_list.py'
else:
    exit()


def get_key(key):
    print('Press the "%s" key.' % key)

    test_command = 'xinput test %s' % sys.argv[2]

    key_pattern = r'key press *[0-9]{1,3} *\|'
    data_length = 1

    p = os.popen(test_command)
    key_data = p.read(data_length)

    while ( re.search(key_pattern, key_data) == None ):
        key_data += p.read(data_length)
        key_data = key_data.replace("\n", "|")

    p.close()

    key_code = int(re.search(key_pattern, key_data).group().split(' ')[-2])

    return key, key_code

f = open(key_list)
keys = [k.strip() for k in f.readlines()]
f.close()

key_map = {}

for key in keys:
    key, key_code = get_key(key)
    key_map[key_code] = key

output = "keymap = " + str(key_map)

f = open(output_file, 'w')
f.write(output)
f.close()
