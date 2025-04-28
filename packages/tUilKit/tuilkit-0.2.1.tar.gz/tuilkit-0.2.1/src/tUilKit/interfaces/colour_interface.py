from abc import ABC, abstractmethod

class ColourInterface(ABC):
    @abstractmethod
    def get_fg_colour(self, colour_code: str) -> str:
        pass

    @abstractmethod
    def strip_ansi(self, fstring: str) -> str:
        pass

    @abstractmethod
    def colour_fstr(self, *args) -> str:
        pass
