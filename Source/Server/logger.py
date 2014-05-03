"""
This file implements a simple logger. The log message are written to stdout and
to the log files. There is a log file for all message, and there are log files
for warning, error and info messages.

Usage: 
------

import logger

logger.log(type, message, time)

Author: Thomas van Ophem, thomas.vanophem@student.uva.nl
Date: 29-04-2014
"""

import os
from time import strftime

# Color codes to print fancy info/warning/error messages.     
colors = {'BUSY' : '\033[1;47m', 'INFO' : '\033[1;46m', 'OK' : '\033[1;42m', 
            'WARNING' : '\033[1;43m', 'ERROR' : '\033[1;41m', 
            'END' : '\033[1;m'}
    
def warning(message, time):
    """
    Logs a warning message.
    """
    
    # Print the warning message to stdout with fancy collors.
    print colors['WARNING'] + time + " WARNING: " + message + colors['END']
    
    # Write the message to the log files.
    with open("./Logs/full_log " + strftime("%d-%m-%y"), "a+") as f:
        f.write(time + " WARNING: " + message + "\n")
    with open("./Logs/Warnings/log " + strftime("%d-%m-%y"), "a+") as f:
        f.write(time + " WARNING: " + message + "\n")
    
def error(message, time):
    """
    Logs an error message.
    """
    
    # Print the error message to stdout with fancy collors.
    print colors['ERROR'] + time + " ERROR: " + message + colors['END']
    
    # Write the message to the log files.
    with open("./Logs/full_log " + strftime("%d-%m-%y"), "a+") as f:
        f.write(time + " ERROR: " + message + "\n")
    with open("./Logs/Errors/log " + strftime("%d-%m-%y"), "a+") as f:
        f.write(time + " ERROR: " + message + "\n")
    
def info(message, time):
    """
    Log an info message.
    """
    
    # Print the info message to stdout with fancy collors.
    print colors['INFO'] + time + " INFO: " + message + colors['END']
    
    # Write the message to the log files.
    with open("./Logs/full_log " + strftime("%d-%m-%y"), "a+") as f:
        f.write(time + " INFO: " + message + "\n")
    with open("./Logs/Info/log " + strftime("%d-%m-%y"), "a+") as f:
        f.write(time + " INFO: " + message + "\n")
    
def busy(message, time):
    """
    Logs a busy message.
    """
    
    # Print the busy message to stdout with fancy collors.
    print colors['BUSY'] + time + " BUSY: " + message + colors['END']
    
    # Write the message to the log file.
    with open("./Logs/full_log " + strftime("%d-%m-%y"), "a+") as f:
        f.write(time + " BUSY: " + message + "\n")
    
def ok(message, time):
    """
    Logs an OK message.
    """
    
    # Print the OK message to stdout with fancy collors.
    print colors['OK'] + time + " OK: " + message + colors['END']
    
    # Write the message to the log file.
    with open("./Logs/full_log " + strftime("%d-%m-%y"), "a+") as f:
        f.write(time + " OK: " + message + "\n")
    
def log(log_type, message, time):
    """
    Main logger function, calls the more specific log functions (e.g. the 
    funtions for warnings, errors etc.).
    
    Usage:
    ------
    
    log(type, message, time)
    
    type in ["warning", "error", "info", "busy", "ok"],
    message is the message to log,
    time a string containing the time of the event.    
    """
    
    # Create log directories if needed.
    if not os.path.isdir("Logs"):
        os.makedirs("Logs");
    if not os.path.isdir("Logs/Warnings"):
        os.makedirs("./Logs/Warnings");
    if not os.path.isdir("Logs/Errors"):
        os.makedirs("./Logs/Errors");
    if not os.path.isdir("Logs/Info"):
        os.makedirs("./Logs/Info");
    
    # Check if the type is valid and log the message or log an error.                
    if log_type in ['warning', 'error', 'info', 'busy', 'ok']:
        eval(log_type + "('" + message + "', '" + time + "')")
    else:
        error("Unknown log type '" + log_type + "' message: '" + message, time)
