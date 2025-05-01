from enum import Enum


class ExtractMethod(str, Enum):
    API = "api"
    HTML = "html"

    def __str__(self) -> str:
        return str(self.value)
