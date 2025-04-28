# {Local Project}/tUilKit/tests/test_module.py
"""
This module contains test functions to verify the soundness of output functions 
from the tUilKit.utils.output module.
"""

import sys
import os
import json

# Ensure the base directory of the project is included in the system path
base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src'))
if base_dir not in sys.path:
    sys.path.insert(0, base_dir)

from tUilKit.utils.output import Logger, ColourManager
from tUilKit.config.config import ConfigLoader

# Load colour config
COLOUR_CONFIG_PATH = os.path.join(base_dir, "tUilKit", "config", "COLOURS.json")
with open(COLOUR_CONFIG_PATH, "r") as f:
    colour_config = json.load(f)

colour_manager = ColourManager(colour_config)
logger = Logger(colour_manager)

# Set up a test log file
TEST_LOG_FILE = os.path.join(os.path.dirname(__file__), "test_output.log")

def test_log_message():
    logger.log_message("This is a plain log message.", log_file=TEST_LOG_FILE)
    print("test_log_message passed.")

def test_colour_log():
    logger.colour_log("INFO", "This is a coloured log message.", log_file=TEST_LOG_FILE)
    print("test_colour_log passed.")

def test_log_done():
    logger.log_done(log_file=TEST_LOG_FILE)
    print("test_log_done passed.")

def test_log_exception():
    try:
        1 / 0
    except Exception as e:
        logger.log_exception("Division by zero", e, log_file=TEST_LOG_FILE)
    print("test_log_exception passed.")

def test_log_column_list():
    import pandas as pd
    df = pd.DataFrame({"A": [1,2], "B": [3,4]})
    logger.log_column_list(df, "dummy.csv", log_file=TEST_LOG_FILE)
    print("test_log_column_list passed.")

def test_print_rainbow_row():
    logger.print_rainbow_row(pattern="X-O-", spacer=2, log_file=TEST_LOG_FILE)
    print("test_print_rainbow_row passed.")

def test_print_borders():
    pattern = {
        "TOP": ["==="],
        "LEFT": ["|"],
        "RIGHT": ["|"],
        "BOTTOM": ["==="]
    }
    logger.print_top_border(pattern, 20, log_file=TEST_LOG_FILE)
    logger.print_text_line("Bordered Text", pattern, 20, log_file=TEST_LOG_FILE)
    logger.print_bottom_border(pattern, 20, log_file=TEST_LOG_FILE)
    print("test_print_borders passed.")

def test_apply_border():
    pattern = {
        "TOP": ["==="],
        "LEFT": ["|"],
        "RIGHT": ["|"],
        "BOTTOM": ["==="]
    }
    logger.apply_border("Hello, bordered world!", pattern, total_length=30, log_file=TEST_LOG_FILE)
    print("test_apply_border passed.")

# List of (test_number, test_name, test_function)
TESTS = [
    (1, "test_log_message", test_log_message),
    (2, "test_colour_log", test_colour_log),
    (3, "test_log_done", test_log_done),
    (4, "test_log_exception", test_log_exception),
    (5, "test_log_column_list", test_log_column_list),
    (6, "test_print_rainbow_row", test_print_rainbow_row),
    (7, "test_print_borders", test_print_borders),
    (8, "test_apply_border", test_apply_border),
]

if __name__ == "__main__":
    # Clean up log file before running tests
    if os.path.exists(TEST_LOG_FILE):
        os.remove(TEST_LOG_FILE)

    results = []
    for num, name, func in TESTS:
        try:
            func()
            results.append((num, name, True))
        except Exception as e:
            logger.log_exception(f"{name} failed", e, log_file=TEST_LOG_FILE)
            print(f"{name} failed: {e}")
            results.append((num, name, False))

    total_count = len(TESTS)
    count_successes = sum(1 for _, _, passed in results if passed)
    count_unsuccessfuls = total_count - count_successes

    logger.colour_log("DONE", "Successful tests:", "OUTPUT", f"{count_successes} / {total_count}")
    if count_unsuccessfuls > 0:
        logger.colour_log("WARN", "Unsuccessful tests:", "ERROR", count_unsuccessfuls, "OUTPUT", f"/ {total_count}")
        for num, name, passed in results:
            if not passed:
                logger.colour_log("LIST", f"Test {num}: {name} ","ERROR","FAILED")
    else:
        logger.colour_log("DONE", "Unsuccessful tests:", "OUTPUT", f"{count_unsuccessfuls} / {total_count}")
        logger.colour_log("DONE", "All tests passed!")

