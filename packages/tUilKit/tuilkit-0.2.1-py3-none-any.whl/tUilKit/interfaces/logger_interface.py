from abc import ABC, abstractmethod

class LoggerInterface(ABC):
    @abstractmethod
    def log_message(self, message: str, log_file: str = None, end: str = "\n") -> None:
        pass

    @abstractmethod
    def log_exception(self, description: str, exception: Exception, log_file: str = None) -> None:
        pass

    @abstractmethod
    def log_done(self, log_file: str = None, end: str = "\n") -> None:
        pass

    @abstractmethod
    def colour_log(self, *args, spacer=0, log_file=None, end="\n"):
        pass

    @abstractmethod
    def log_column_list(self, df, filename, log_file=None):
        pass

    @abstractmethod
    def print_rainbow_row(self, pattern="X-O-", spacer=0, log_file=None, end="\n"):
        pass

    @abstractmethod
    def print_top_border(self, pattern, length, index=0, log_file=None, border_colour='RESET'):
        pass

    @abstractmethod
    def print_text_line(self, text, pattern, length, index=0, log_file=None, border_colour='RESET', text_colour='RESET'):
        pass

    @abstractmethod
    def print_bottom_border(self, pattern, length, index=0, log_file=None, border_colour='RESET'):
        pass

    @abstractmethod
    def apply_border(self, text, pattern, total_length=None, index=0, log_file=None, border_colour='RESET', text_colour='RESET'):
        pass