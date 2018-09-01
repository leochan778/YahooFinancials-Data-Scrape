#!/usr/bin/env python3

# Handles basic error logging

import os.path
from datetime import datetime 

def write_error(error):
    date = datetime.now()
    error_log = "error_log.txt"
    error_message = f"\nError recorded on {date}.\n{error}\n======================================"
    
    if os.path.exists(error_log):
        with open(error_log, "a") as file:
            file.write(f"\n{error_message}")
    else:
        with open(error_log, "w") as file:
            file.write(f"ERROR LOG\n{error_message}")
    file.close()