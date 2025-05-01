from enum import Enum


class SourceCollectType(str, Enum):
    DATA = "data"
    METADATA = "metadata"

    def __str__(self) -> str:
        return str(self.value)
