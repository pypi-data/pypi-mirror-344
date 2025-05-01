from enum import Enum


class InputSourceEnum(str, Enum):
    AI = "AI"
    MANUAL = "manual"
    MODERATOR = "moderator"

    def __str__(self) -> str:
        return str(self.value)
