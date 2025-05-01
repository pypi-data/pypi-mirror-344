from enum import Enum


class CustomFieldType(str, Enum):
    COMMENT = "comment"
    CONTENT = "content"

    def __str__(self) -> str:
        return str(self.value)
