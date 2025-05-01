from enum import Enum


class IntervalType(str, Enum):
    DAY = "day"
    WEEK = "week"

    def __str__(self) -> str:
        return str(self.value)
