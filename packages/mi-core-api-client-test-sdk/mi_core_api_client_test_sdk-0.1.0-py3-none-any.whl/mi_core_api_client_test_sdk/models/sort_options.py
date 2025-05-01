from enum import Enum


class SortOptions(str, Enum):
    HOT = "hot"
    NEW = "new"
    RISING = "rising"
    TOP = "top"

    def __str__(self) -> str:
        return str(self.value)
