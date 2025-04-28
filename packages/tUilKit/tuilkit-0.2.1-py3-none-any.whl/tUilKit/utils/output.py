# {Local Project}/tUilKit/src/tUilKit/utils/output.py
"""
Contains functions for log files and displaying text output in the terminal using ANSI sequences to colour code output.
 
"""
import re
from datetime import datetime
import sys
import os
from abc import ABC, abstractmethod

# Add the base directory of the project to the system path
base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..\\..\\'))
if base_dir not in sys.path:
    sys.path.insert(0, base_dir)

from tUilKit.dict.DICT_COLOURS import RGB
from tUilKit.dict.DICT_CODES import ESCAPES, COMMANDS
from tUilKit.interfaces.logger_interface import LoggerInterface
from tUilKit.interfaces.colour_interface import ColourInterface
from tUilKit.config.config import ConfigLoader

# ANSI ESCAPE CODE PREFIXES for colour coding f-strings

SET_FG_COLOUR = ESCAPES['OCTAL'] + COMMANDS['FGC']
SET_BG_COLOUR = ESCAPES['OCTAL'] + COMMANDS['BGC']
ANSI_RESET = ESCAPES['OCTAL'] + COMMANDS['RESET']

config_loader = ConfigLoader()
colour_config = config_loader.load_config(config_loader.get_json_path('COLOURS.json'))
ANSI_FG_COLOUR_SET = {key: f"{ESCAPES['OCTAL']}{COMMANDS['FGC']}{RGB[value]}" for key, value in colour_config['COLOUR_KEY'].items()}

"""
Function to retrieve the custom colour code from the COLOURS.json file
RGB Hex values are hardcoded in the dict.DICT_COLOURS module in the RGB dictionary 
and converted to ANSI escape codes in the utils.output module.
"""
def get_fg_colour(colour_code):
    return ANSI_FG_COLOUR_SET.get(colour_code, ANSI_FG_COLOUR_SET['RESET'])

# Function to remove ANSI escape codes from a string
def strip_ansi(fstring):
    ansi_escape = re.compile(r"\x1B\[[0-?]*[ -/]*[@-~]")
    return ansi_escape.sub('', fstring)

# Function to append the current time to a string
def append_time(fstring=""):
    if fstring != "":
        time_string = f"{fstring} {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    else:
        # If fstring is empty, just return the current time
        time_string = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    return time_string

# Function to split a time string into date and time components
def split_time_string(time_string): 
    datetime_part = time_string.split(" ")[-1] 
    date_part = time_string.split(" ")[-2] 
    return date_part, datetime_part

# Function to log a message to the console and an optional log file
def log_message(message, log_file=None, end="\n"):
    print(message, end=end)
    if log_file:
        with open(log_file, 'a') as log:
            log.write(strip_ansi(message) + end)

# # Function to concatenate colour codes with text using f-strings
def colour_fstr(*args):
    result = ""
    RESET = get_fg_colour('RESET')
    current_colour = RESET

    for i, arg in enumerate(args):
        # Handle lists by joining their elements into a single string
        if isinstance(arg, list):
            arg = ', '.join(map(str, arg))
        
        # Check if the argument is a valid colour key
        if arg in ANSI_FG_COLOUR_SET:
            current_colour = get_fg_colour(arg)
        else:
            # Append the argument with the current colour
            result += f"{current_colour}{arg}"
            # Add a space after the argument if it's not the last one
            if i != len(args) - 1:
                result += " "
            current_colour = RESET

    # Reset the colour at the end
    result += RESET
    return result

class Logger(LoggerInterface):
    def __init__(self, colour_manager=None):
        self.colour_manager = colour_manager

    def log_message(self, message: str, log_file: str = None, end: str = "\n") -> None:
        print(message, end=end)
        if log_file:
            with open(log_file, 'a') as log:
                log.write(message + end)

    def log_exception(self, description: str, exception: Exception, log_file: str = None) -> None:
        self.log_message("", log_file=log_file)
        self.colour_log("ERROR", "UNEXPECTED ERROR:", "INFO", description, "ERROR", str(exception), log_file=log_file)
        self.log_message(f"ERROR: {description} - {exception}", log_file)

    def log_done(self, log_file: str = None, end: str = "\n") -> None:
        self.log_message (colour_fstr("DONE","Done! "), log_file=log_file, end=end)

    def colour_log(self, *args, spacer=0, log_file=None, end="\n"):
        # Function to log a message with colour and optional spacer to screen and optional log file
        date, time = split_time_string(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        if spacer > 0:
            coloured_message = colour_fstr("DATE", date, "TIME", time, f"{' ' * spacer}", *args)
        else:
            coloured_message = colour_fstr("DATE", date, "TIME", time, *args)
        log_message(coloured_message, log_file=log_file, end=end)

    def log_column_list(self, df, filename, log_file=None):
        # Function to colour log a column list for a dataframe
        self.colour_log(
            "PATH", os.path.dirname(filename),"/",
            "FILE", os.path.basename(filename),
            ": ",
            "INFO", "Columns:",
            "OUTPUT", df.columns.tolist(),
            log_file=log_file)

    def print_rainbow_row(self, pattern="X-O-", spacer=0, log_file=None, end="\n"):
        # Function to print a rainbow row with a pattern and optional spacer
        # Define the bright colours in hue order
        bright_colours = [
            'RED', 'CRIMSON', 'ORANGE', 'CORAL', 'GOLD', 
            'YELLOW', 'CHARTREUSE', 'GREEN', 'CYAN', 
            'BLUE', 'INDIGO', 'VIOLET', 'MAGENTA'
        ]

        # Create spacer
        self.log_message(f"{' ' * spacer}", log_file=log_file, end="")

        # Combine the colours in forward and reverse order
        rainbow_colours = bright_colours + bright_colours[::-1][1:-1]

        # Print a patterned row in different rainbow colours
        for colour in rainbow_colours:
            self.log_message(colour_fstr(colour, pattern), log_file=log_file, end="")
        self.log_message(colour_fstr("RED", f"{pattern}"[0]), log_file=log_file, end=end)  # New line at the end

    def print_top_border(self, pattern, length, index=0, log_file=None, border_colour='RESET'):
        # Function to print the top border
        # Calculate the number of repetitions needed to fill the length
        top = pattern['TOP'][index] * (length // len(pattern['TOP'][index]))
        self.log_message(colour_fstr(border_colour, f" {top}"), log_file=log_file)

    def print_text_line(self, text, pattern, length, index=0, log_file=None, border_colour='RESET', text_colour='RESET'):
        # Function to print the text line with left and right borders
        left = pattern['LEFT'][index]
        right = pattern['RIGHT'][index]
        inner_text_length = len(left) + len(text) + len(right)
        trailing_space_length = length - inner_text_length - 1
        text_line_args = [border_colour, left, text_colour, text, f"{' ' * trailing_space_length}", border_colour, right]
        self.log_message(colour_fstr(*text_line_args), log_file=log_file)

    def print_bottom_border(self, pattern, length, index=0, log_file=None, border_colour='RESET'):
        # Function to print the bottom border
        bottom = pattern['BOTTOM'][index] * (length // len(pattern['BOTTOM'][index]))
        self.log_message(colour_fstr(border_colour, f" {bottom}"), log_file=log_file)

    def apply_border(self, text, pattern, total_length=None, index=0, log_file=None, border_colour='RESET', text_colour='RESET'):
        # Combined function to apply borders
        inner_text_length = len(pattern['LEFT'][index]) + len(text) + len(pattern['RIGHT'][index])    
        if total_length and total_length > inner_text_length:
            length = total_length
        else:
            length = inner_text_length

        self.print_top_border(pattern, length, index, log_file=log_file, border_colour=border_colour)
        self.print_text_line(text, pattern, length, index, log_file=log_file, border_colour=border_colour, text_colour=text_colour)
        self.print_bottom_border(pattern, length, index, log_file=log_file, border_colour=border_colour)

class ColourManager(ColourInterface):
    def __init__(self, colour_config: dict):
        self.ANSI_FG_COLOUR_SET = {
            key: f"\033[38;2;{value}" for key, value in colour_config['COLOUR_KEY'].items()
        }

    def get_fg_colour(self, colour_code: str) -> str:
        return self.ANSI_FG_COLOUR_SET.get(colour_code, "\033[0m")

    def strip_ansi(self, fstring: str) -> str:
        ansi_escape = re.compile(r"\x1B\[[0-?]*[ -/]*[@-~]")
        return ansi_escape.sub('', fstring)

    def colour_fstr(self, *args) -> str:
        result = ""
        # ANSI escape code for resetting foreground colour
        FG_RESET = "\033[38;2;190;190;190m"
        # current_colour = FG_RESET
        for arg in args:
            if arg in self.ANSI_FG_COLOUR_SET:
                current_colour = self.get_fg_colour(arg)
            else:
                result += f"{current_colour}{arg}"
        result += FG_RESET
        return result
