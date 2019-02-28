xinput-keylog-decoder
=====================

Decode keylogs created with xinput into a human-readable format.


Description
-----------

`xinput` is a program that can be used to log keystrokes on the Linux desktop and is installed by default with several popular Linux distributions including Ubuntu, Fedora, and many of their derivatives. However, as you can see below, the raw xinput output isn't especially easy to understand on its own.

```
ubuntu@ubuntu:~$ xinput test 5 | tee test.txt
key release 36 
key press   50 
key press   33 
key release 33 
key release 50 
key press   38 
key release 38 
...

```

`xinput-keylog-decoder` converts the numeric key codes output by `xinput` to the more human-friendly output shown below. It also attempts to handle unrecognized lines such as time and date stamps gracefully when they are detected in the log file.

```
ubuntu@ubuntu:~$ ./xinput-keylog-decoder.py test.txt 
<LSHIFT>+password1<LSHIFT>+1<LCTRL>+c
```


Included files
--------------

| Filename | Description |
|----------|-------------|
| `README.md` | This file
| `config/key-list.chars.txt` | Labels for each regular/character key, one per line. An example file is included for the standard 104 key US layout.
| `config/key-list.mods.txt` | Labels for each modifier key, one per line. An example file is included for the standard 104 key US layout.
| `generate-keymap.py` | Keymap-generation script. Matches key labels in the two key-list files to numeric key codes to generate keymaps.
| `xinput-keylog-decoder.py` | The main program file that decodes xinput keylogs
| `simple_decoder.py` | A simpler version of the decoder script useful for debugging or detailed analysis of xinput log files
| `start-logging.sh` | An example script that attempts to automatically identify hardware keyboards attached to the system and log keystrokes
| `stop-logging.sh` | A script used to kill all keylogging processes started by `start-logging.sh`


Steps for use
-------------

1. Generate keymap files that match the layout of the target keyboard. This is done by:
    1. Save each key name in `config/key-list.chars.txt` and `config/key-list.mods.txt`, one per line. Keys can be listed in both files if they have both standalone and modifier functions, for example, the Windows key.
    2. Run `generate-keymap.py` to match xinput key codes to the key names listed in each of the key-list files. This script will need to be run twice - once to generate the character key map and once to generate the modifier key map. Note that pressing the keys when prompted by the script will cause different actions to take place on your own desktop (e.g. opening the Help window when you press F1).
2. Log keys on the target system with `xinput`
3. Decode the keylog file with `xinput-keylog-decoder.py`
