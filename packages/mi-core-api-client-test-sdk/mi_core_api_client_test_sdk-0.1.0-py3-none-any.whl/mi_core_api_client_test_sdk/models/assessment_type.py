from enum import Enum


class AssessmentType(str, Enum):
    AWESOME = "awesome"
    BAD = "bad"
    GOOD = "good"
    OK = "ok"
    VERY_BAD = "very_bad"

    def __str__(self) -> str:
        return str(self.value)
