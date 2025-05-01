from enum import Enum


class StoryboardGenerationStatusEnum(str, Enum):
    CREATED = "created"
    ERROR = "error"
    FINISHED = "finished"
    IN_PROGRESS = "in progress"

    def __str__(self) -> str:
        return str(self.value)
