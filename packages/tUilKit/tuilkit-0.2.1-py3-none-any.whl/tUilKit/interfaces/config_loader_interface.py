from abc import ABC, abstractmethod

class ConfigLoaderInterface(ABC):
    @abstractmethod
    def load_config(self, json_file_path: str) -> dict:
        pass

    @abstractmethod
    def get_json_path(self, file: str, cwd: bool = False) -> str:
        pass