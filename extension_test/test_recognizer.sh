#!/usr/bin/env bash

# PASTED FROM cmulab_elan_extension.sh:
# It seems that recognizer processes invoked by ELAN don't inherit any regular
# environmental variables (like PATH), which makes it difficult to track down
# where both Python and ffmpeg(1) might be.  These same processes also have
# their locale set to C.  This implies a default ASCII file encoding.
export LC_ALL="en_US.UTF-8"
export PYTHONIOENCODING="utf-8"

which python3
python3 --version
python3 -c 'import tkinter; tcl = tkinter.Tcl(); print(tcl.call("info", "patchlevel"))'
python3 -c 'import tkinter; root = tkinter.Tk(); print(root.tk.call("info", "patchlevel"))'

# If you want to set up a virtual environment:
# python3 -m venv venv
# source venv/bin/activate
# python3 -m pip install -r requirements.txt

echo "Running test_recognizer.sh..."

# cd to the script directory
cd "$(dirname "$0")"

if [ ! -d "venv" ]; then
    echo "PROGRESS: 1% (Initial setup) Creating virtual env, installing dependencies"
    python3 -m venv venv
    source venv/bin/activate
    python3 -m pip --no-input install -r requirements.txt
    echo "PROGRESS: 5% One-time initialization successfully completed!"
    deactivate
fi

source venv/bin/activate

# Run the Python script, piping in any parameters from ELAN
python3 test_recognizer.py
