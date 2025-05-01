from enum import Enum


class JobStatus(str, Enum):
    COMPLETED = "completed"
    CREATED = "created"
    FAILED = "failed"
    PROCESSING = "processing"

    def __str__(self) -> str:
        return str(self.value)
