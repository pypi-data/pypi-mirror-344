from enum import Enum


class ExecutionStatus(str, Enum):
    COMPLETED = "completed"
    CREATED = "created"
    FAILED = "failed"
    INITIALIZED = "initialized"
    PROCESSING = "processing"
    TERMINATED = "terminated"

    def __str__(self) -> str:
        return str(self.value)
