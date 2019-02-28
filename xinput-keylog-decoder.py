#!/usr/bin/env python3

import sys

# Import key mappings for modifier keys from config/cfg_mod_list.py
import config.cfg_mod_list
mod_keymap = config.cfg_mod_list.keymap

# Import key mappings for character (non-modifier) keys from 
# config/cfg_char_list.py
import config.cfg_char_list
char_keymap = config.cfg_char_list.keymap


# Parse the given line in the context of the two provided keymaps.
# Returns a dictionary containing:
# {
#     "action": Contains the string "press" or "release" if a known key action is #               detected. Contains None if the line does not contain a known key
#               action.
#
#     "key": A string containing the human-readable key character or key name.
#            If the line can't be parsed as a key press or release, the entire
#            line is returned in the string.
#
#     "type": An array containing one or more of "char" and "mod" based on which
#             keymap files contained the key. If neither keymap contains the
#             key, both "char" and "mod" are included in the array.
# }
def parse_line(line, char_keymap=char_keymap, mod_keymap=mod_keymap):

    key_type = []

    if "key press" in line or "key release" in line:

        # Store the key name in key
        key_num = int(line.split(" ")[-1])
        if char_keymap.get(key_num):
            key = char_keymap.get(key_num)
            key_type.append("char")
        if mod_keymap.get(key_num):
            key = mod_keymap.get(key_num)
            key_type.append("mod")
        if key_num not in mod_keymap and key_num not in char_keymap:
            key = "<UNKNOWN KEY: %s>" % key_num
            key_type += ["char", "mod"]
    else:
        key_type = None
        key = line

    # Determine the action recorded in the line
    if "key press" in line:
        action="press"
    elif "key release" in line:
        action="release"
    else:
        action=None

    this_key = { "action": action, "key": key, "type": key_type }
    return this_key


usage = """
xinput-keylog-decoder
---------------------

Converts logs created with xinput into human-readable keylogs.

Usage: python3 xinput-keylog-decoder.py <xinput log file>
"""

if len(sys.argv) <= 1 or "-h" in sys.argv or "--help" in sys.argv:
    print(usage)
    exit()

if len(sys.argv) > 1: log_file = sys.argv[1]
f = open(log_file)
log_data = [line.strip() for line in f.readlines()]
f.close()

# These variables are used to keep track of the line currently being processed
# (line), the next line to be processed (next_line), and modifier keys that are
# currently held down (pressed_keys).
line = ""
next_line = ""
pressed_keys = []

# These two variables are used to help with printing non-key lines of output.
first_line = True
last_line_raw = True

# This is a fix for the for loop below to make sure it processes all lines of
# the log file since it doesn't process the last line stored in the log_data
# array.
log_data.append("---END OF LOG---")


# Process each line in the log file
for next_line in log_data:
    
    # Read the first two lines into variables before continuing so that each
    # line in the log can be interpreted in the context of the line that follows
    # it.
    if line == None:
        line = next_line    
        continue

    this_key = parse_line(line)
    next_key = parse_line(next_line)


    # Handle key presses
    if this_key["action"] == "press":
        
        # If no modifier keys are currently held down:
        if len(pressed_keys) == 0 :
        
            # If this isn't a modifier key, or if it is a modifier key but it
            # is released before any other keys are pressed, just print the
            # key.
            if ( ( "mod" not in this_key["type"] ) or  
                 ( next_key["key"] == this_key["key"] and 
                   next_key["action"] == "release" ) ):
               print(this_key["key"], end='')
    
        # Else, if modifier keys are currently held down:
        else:
            print("+".join(pressed_keys) + "+" + this_key["key"], end='')
    
        # If the currently pressed key is a modifier key, add it to the array
        # of pressed keys. It will be automatically removed from the array
        # when it is released on a subsequent line.
        if "mod" in this_key["type"]:
            pressed_keys.append(this_key["key"])

        # Adjust variables used for formatting non-key press/release output
        first_line = False      # The next line processed will not be the first
                                # line of the log file
        last_line_raw = False   # This line was successfully processed as a key


    # Handle key releases        
    elif this_key["action"] == "release":
    
        # As keys are released, remove them from the pressed_keys array
        if this_key["key"] in pressed_keys:
            pressed_keys.remove(this_key["key"])
    
        # Adjust variables used for formatting non-key press/release output
        first_line = False      # The next line processed will not be the first
                                # line of the log file
        last_line_raw = False   # This line was successfully processed as a key

           
    # Finally, handle any lines that are not key presses or key releases
    elif this_key["key"] != None and this_key["key"] != "":
    
        # Depending on the nature of previously printed output, print blank
        # lines to add some space before the next output
        if not first_line:
            print()
        if not last_line_raw:
            print()
            
        # Print the raw string contained in this line of the log file
        print(this_key["key"])
        
        # Adjust variables used for formatting non-key press/release output
        first_line = False      # The next line processed will not be the first
                                # line of the log file
        last_line_raw = True    # This line contained non-key data that was 
                                # handled as a raw string

        # Print a blank line if the next line of the log file contains a key
        # press or release
        if next_key["action"] != None:
            print()


    # Move next_line into line before the next line of the log file is read
    line = next_line


# Print a newline at the end of the script to tidy up the output
print()
