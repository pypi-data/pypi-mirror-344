# {Local Project}/tUilKit/tests/test_module.py
"""
This module contains test functions to verify the soundness of interfaces and their implementations.
It also tests folder creation and initialization sequences for a Test_NewProject folder.
"""
import os
import sys
import json

# Ensure the src directory is in sys.path
base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src'))
if base_dir not in sys.path:
    sys.path.insert(0, base_dir)

# Now import interfaces and implementations from your local codebase
from tUilKit.interfaces.logger_interface import LoggerInterface
from tUilKit.interfaces.colour_interface import ColourInterface
from tUilKit.interfaces.file_system_interface import FileSystemInterface
from tUilKit.interfaces.config_loader_interface import ConfigLoaderInterface

from tUilKit.utils.output import Logger, ColourManager
from tUilKit.utils.fs import FileSystem
from tUilKit.config.config import ConfigLoader

# Load colour config from the correct path
COLOUR_CONFIG_PATH = os.path.join(base_dir, "tUilKit", "config", "COLOURS.json")
with open(COLOUR_CONFIG_PATH, "r") as f:
    colour_config = json.load(f)

colour_manager = ColourManager(colour_config)
logger = Logger(colour_manager)
file_system = FileSystem(logger)
config_loader = ConfigLoader()

# Define the test folder path
TEST_FOLDER = os.path.join(os.path.dirname(__file__), "Test_NewProject")

def test_folder_creation():
    """
    Test the creation of the Test_NewProject folder.
    """
    log_file = os.path.join(TEST_FOLDER, "test_folder_creation.log")
    logger.log_message("Starting test: test_folder_creation", log_file)

    # Validate and create the Test_NewProject folder
    file_system.validate_and_create_folder(TEST_FOLDER, log_file)
    assert os.path.exists(TEST_FOLDER), f"Test folder {TEST_FOLDER} was not created."

    logger.log_message("Test folder creation passed!", log_file)

def test_config_loading():
    """
    Test the loading of configuration files.
    """
    log_file = os.path.join(TEST_FOLDER, "test_config_loading.log")
    logger.log_message("Starting test: test_config_loading", log_file)

    # Load the global configuration
    global_config = config_loader.load_config(config_loader.get_json_path('GLOBAL_CONFIG.json'))
    assert "FOLDERS" in global_config, "FOLDERS key missing in global configuration."
    assert "FILES" in global_config, "FILES key missing in global configuration."

    logger.log_message("Configuration loading passed!", log_file)

def test_file_operations():
    """
    Test file operations in the Test_NewProject folder.
    """
    log_file = os.path.join(TEST_FOLDER, "test_file_operations.log")
    logger.log_message("Starting test: test_file_operations", log_file)

    # Create a test file
    test_file_path = os.path.join(TEST_FOLDER, "test_file.txt")
    with open(test_file_path, "w") as f:
        f.write("This is a test file.")

    # Verify the file exists
    assert os.path.exists(test_file_path), f"Test file {test_file_path} was not created."

    # List files in the folder
    files = file_system.get_all_files(TEST_FOLDER)
    assert "test_file.txt" in files, "Test file not found in folder."

    logger.log_message("File operations passed!", log_file)

def test_make_folders():
    """
    Test creating all folders specified in MAKE_FOLDERS inside Test_NewProject.
    """
    log_file = os.path.join(TEST_FOLDER, "test_make_folders.log")
    logger.log_message("Starting test: test_make_folders", log_file)

    # Load the global configuration
    global_config = config_loader.load_config(config_loader.get_json_path('GLOBAL_CONFIG.json'))
    make_folders = global_config.get("MAKE_FOLDERS", {})

    # Create each folder inside Test_NewProject
    for folder_name in make_folders.values():
        folder_path = os.path.join(TEST_FOLDER, folder_name)
        file_system.validate_and_create_folder(folder_path, log_file)
        assert os.path.exists(folder_path), f"Folder {folder_path} was not created."

    logger.log_message("MAKE_FOLDERS creation passed!", log_file)

# List of (test_number, test_name, test_function)
TESTS = [
    (1, "test_folder_creation", test_folder_creation),
    (2, "test_config_loading", test_config_loading),
    (3, "test_file_operations", test_file_operations),
    (4, "test_make_folders", test_make_folders),
]

if __name__ == "__main__":
    # Ensure the Test_NewProject folder is clean
    if os.path.exists(TEST_FOLDER):
        for file in os.listdir(TEST_FOLDER):
            file_path = os.path.join(TEST_FOLDER, file)
            try:
                if os.path.isfile(file_path):
                    os.remove(file_path)
                elif os.path.isdir(file_path):
                    import shutil
                    shutil.rmtree(file_path)
            except Exception as e:
                print(f"Failed to remove {file_path}: {e}")
    else:
        os.makedirs(TEST_FOLDER)

    # Run and count tests
    results = []
    for num, name, func in TESTS:
        try:
            func()
            results.append((num, name, True))
        except Exception as e:
            logger.log_exception(f"{name} failed", e)
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

