from abc import ABC, abstractmethod

class FileSystemInterface(ABC):
    @abstractmethod
    def validate_and_create_folder(self, folder_path: str, log_file: str = None) -> bool:
        pass

    @abstractmethod
    def remove_empty_folders(self, path: str, log_file: str = None) -> None:
        pass

    @abstractmethod
    def get_all_files(self, folder: str) -> list[str]:
        pass