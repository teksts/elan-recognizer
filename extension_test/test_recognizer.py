#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
A minimal Python script that:
1) Reads tier input/output parameters from stdin (ELAN).
2) Logs them to a text file (my_minimal_recognizer_output.txt).
3) Displays a PySimpleGUI popup with details (optional).
4) Writes a new tier file with the same annotations.
"""

import sys
import re
import datetime
import PySimpleGUI as sg  # If you prefer no GUI, you can remove this import & usage

def main():
    # Prepare a log file in the current directory
    # (If you need a different location, adjust the path below)
    log_filename = "test_recognizer_output.txt"

    # Open/append to the log file
    with open(log_filename, "a", encoding="utf-8") as log_file:
        now_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_file.write(f"\n---\n[{now_str}] Starting my_minimal_recognizer.py\n")

        input_tier_file = None
        output_tier_file = None
        
        # Read lines from stdin looking for <param name="...">...</param>
        for line in sys.stdin:
            match = re.search(r'<param name="(.*?)".*?>(.*?)</param>', line)
            if match:
                param_name = match.group(1)
                param_value = match.group(2)
                
                if param_name == "input_tier":
                    input_tier_file = param_value.strip()
                elif param_name == "output_tier":
                    output_tier_file = param_value.strip()
        
        # Log the params
        log_file.write(f"  input_tier  = {input_tier_file}\n")
        log_file.write(f"  output_tier = {output_tier_file}\n")

        if not input_tier_file or not output_tier_file:
            msg = "RESULT: FAILED. Missing input_tier or output_tier parameter."
            print(msg)
            log_file.write(msg + "\n")
            # Optional: show a popup
            sg.popup(msg, title="my_minimal_recognizer Error")
            sys.exit(1)
        
        # Read and parse the input tier
        annotations = []
        try:
            with open(input_tier_file, "r", encoding="utf-8") as f:
                for line in f:
                    # Example: <span start="1.0" end="2.5"><v>some text</v></span>
                    m = re.search(r'<span start="(.*?)" end="(.*?)"><v>(.*?)</v>', line)
                    if m:
                        start = m.group(1)
                        end = m.group(2)
                        val = m.group(3)
                        annotations.append((start, end, val))
        except Exception as e:
            msg = f"Failed to read input tier: {e}"
            print(msg)
            log_file.write(msg + "\nRESULT: FAILED.\n")
            sg.popup(msg, title="my_minimal_recognizer Error")
            sys.exit(1)
        
        # Log what we found
        log_file.write("Annotations from the input tier:\n")
        for (start, end, val) in annotations:
            log_file.write(f"  start={start}, end={end}, value={val}\n")

        # Output Tier
        try:
            with open(output_tier_file, "w", encoding="utf-8") as out:
                out.write('<?xml version="1.0" encoding="UTF-8"?>\n')
                out.write('<TIER columns="DemoTier">\n')
                for (start, end, val) in annotations:
                    out.write(f'    <span start="{start}" end="{end}"><v>{val}</v></span>\n')
                out.write('</TIER>\n')
        except Exception as e:
            msg = f"Failed to write output tier: {e}"
            print(msg)
            log_file.write(msg + "\nRESULT: FAILED.\n")
            sg.popup(msg, title="my_minimal_recognizer Error")
            sys.exit(1)
        
        # Show a PySimpleGUI popup of the results (Optional)
        # This might block until the user clicks "OK." If you don't want that, remove it.
        msg = f"Processed {len(annotations)} annotation(s).\nWrote output to:\n{output_tier_file}\n"
        sg.popup(msg, title="my_minimal_recognizer")
        
        # If everything went well
        print("RESULT: DONE.")
        log_file.write("RESULT: DONE.\n")


if __name__ == "__main__":
    main()
