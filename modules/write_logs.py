#!/usr/bin/env python3

# Logs important info

import os.path
from datetime import datetime 

def write_log_entry(entry):
    date = datetime.now()
    logs_file = "logs.txt"
    log_entry = f"{date}: {entry}"
    
    if os.path.exists(logs_file):
        with open(logs_file, "a") as f:
            f.write(f"\n{log_entry}")
    else:
        with open(logs_file, "w") as f:
            f.write(f"LOG FILE (Created on {date})\n{log_entry}")