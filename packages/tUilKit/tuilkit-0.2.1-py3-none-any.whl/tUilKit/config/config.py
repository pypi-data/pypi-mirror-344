# {Local Project}/tUilKit/src/tUilKit/config/config.py
"""
    Load JSON configuration of GLOBAL variables.
"""
import os
import json
from tUilKit.utils.fs import validate_and_create_folder
from tUilKit.interfaces.config_loader_interface import ConfigLoaderInterface


class ConfigLoader(ConfigLoaderInterface):
    def get_json_path(self, file: str, cwd: bool = False) -> str:
        if cwd:
            local_path = os.path.join(os.getcwd(), file)
            if os.path.exists(local_path):
                return local_path
        return os.path.join(os.path.dirname(__file__), file)

    def load_config(self, json_file_path: str) -> dict:
        with open(json_file_path, 'r') as f:
            return json.load(f)


# Only load GLOBAL_CONFIG.json
config_loader = ConfigLoader()
global_config = config_loader.load_config(config_loader.get_json_path('GLOBAL_CONFIG.json'))
# column_mapping = config_loader.load_config(config_loader.get_json_path('COLUMN_MAPPING.json'))

LOG_FILE = f"{global_config['FOLDERS']['TEST_LOG_FILES']}{global_config['FILES']['INIT_LOG']}"


