from enum import Enum


class TimeRange(str, Enum):
    VALUE_0 = "1 month"
    VALUE_1 = "1 year"
    VALUE_2 = "5 years"

    def __str__(self) -> str:
        return str(self.value)
