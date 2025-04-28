# {Local Project}/tUilKit/src/tUilKit/utils/fs.py
"""
Contains functions for managing files, folders and path names
""" 
import shutil
import os
from tUilKit.interfaces.file_system_interface import FileSystemInterface

class FileSystem(FileSystemInterface):
    def __init__(self, logger):
        self.logger = logger

    def validate_and_create_folder(self, folder_path: str, log_file: str = None) -> bool:
        if not os.path.exists(folder_path):
            self.logger.log_message(f"Creating folder: {folder_path}", log_file)
            os.makedirs(folder_path, exist_ok=True)
        return True

    def remove_empty_folders(self, path: str, log_file: str = None) -> None:
        for root, dirs, files in os.walk(path, topdown=False):
            for dir in dirs:
                dir_path = os.path.join(root, dir)
                if not os.listdir(dir_path):
                    os.rmdir(dir_path)
                    self.logger.log_message(f"Removed empty folder: {dir_path}", log_file)

    def get_all_files(self, folder: str) -> list[str]:
        return [f for f in os.listdir(folder) if os.path.isfile(os.path.join(folder, f))]

# def display_path(path):
#     SHOW_FULL_PATH = init_show_full_path()
#     if SHOW_FULL_PATH == "yes":
#         return path
#     else:
#         return os.path.basename(path)

def validate_and_create_folder(folder_path, log_file=None, logger=None):
    if not os.path.exists(folder_path):
        if logger:
            logger.log_message(f"Attempting to create folder: {folder_path}", log_file)
        try:
            os.makedirs(folder_path, exist_ok=True)
            if logger:
                logger.log_message(f"Created folder: {folder_path}", log_file)
        except Exception as e:
            if logger:
                logger.log_exception("Could not create folder: ", e, log_file=log_file)
            exit(1)
    return True

def validate_extension(fullfilepath, extension):
    base, ext = os.path.splitext(fullfilepath)
    if ext.lower() != extension.lower():                      # Need to append file extension
        fullfilepath += extension
        base, ext = os.path.splitext(fullfilepath)
    return fullfilepath

def no_overwrite(fullfilepath, max_count=None, log_file=None, logger=None):
    base, ext = os.path.splitext(fullfilepath)
    counter = 1
    new_fullfilepath = fullfilepath
    oldest_file = fullfilepath  # Start with the original file
    oldest_timestamp = os.path.getmtime(fullfilepath) if os.path.exists(fullfilepath) else float('inf')
    
    while os.path.exists(new_fullfilepath):  # Append [<count>] to filename to prevent overwriting file 
        new_fullfilepath = f"{base}({counter}){ext}"
        if os.path.exists(new_fullfilepath):
            file_timestamp = os.path.getmtime(new_fullfilepath)
            if file_timestamp < oldest_timestamp:
                oldest_timestamp = file_timestamp
                oldest_file = new_fullfilepath
        counter += 1
        if max_count and counter > max_count:
            if logger:
                logger.log_message(f"Max count reached, returning oldest file: {os.path.dirname(oldest_file)}/{os.path.basename(oldest_file)}", log_file)
            return oldest_file
    if logger:
        logger.log_message(f"No-overwrite filename generated: {os.path.dirname(new_fullfilepath)}/{os.path.basename(new_fullfilepath)}", log_file)
    return new_fullfilepath

def backup_and_replace(full_pathname, backup_full_pathname, log_file=None, logger=None):
    if full_pathname and backup_full_pathname:
        if os.path.exists(full_pathname):
            # Create a backup of the original file
            shutil.copy2(full_pathname, backup_full_pathname)
            if logger:
                logger.log_message(f"Backup created: {backup_full_pathname}", log_file)
            
            # Replace the original file
            try:
                with open(full_pathname, 'w') as file:
                    file.write('')
                if logger:
                    logger.log_message(f"File replaced: {full_pathname}", log_file)
            except Exception as e:
                if logger:
                    logger.log_exception("Generated Exception ", e, log_file=log_file)
    return full_pathname

def remove_empty_folders(path, log_file=None, logger=None):
    for root, dirs, files in os.walk(path, topdown=False):
        for dir in dirs:
            dir_path = os.path.join(root, dir)
            if not os.listdir(dir_path):
                try:
                    shutil.rmtree(dir_path)
                    if logger:
                        logger.log_message(f"Removed empty folder: {dir_path}", log_file)
                except Exception as e:
                    if logger:
                        logger.log_message(f"Error removing folder {dir_path}: {e}", log_file)
                        logger.log_exception("Exception produced in ", e, log_file=log_file)

def sanitize_filename(filename):                                # Function to sanitize a filename by replacing invalid characters
    invalid_chars = {
        ':' : '-',
        '\\' : '',
        '/' : '',
        '?' : '',
        '*' : '',
        '<' : '',
        '>' : '',
        '|' : '',
    }
    for char, replacement in invalid_chars.items():
        new_filename = filename.replace(char, replacement)
    return new_filename

def get_all_files(folder):                                      # Return List of all filenames that exist within a folder
    return [f for f in os.listdir(folder) if os.path.isfile(os.path.join(folder, f))]
