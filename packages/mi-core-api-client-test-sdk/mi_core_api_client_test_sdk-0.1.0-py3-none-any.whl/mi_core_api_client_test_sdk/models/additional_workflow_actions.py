from enum import Enum


class AdditionalWorkflowActions(str, Enum):
    CUSTOM_FIELDS = "custom_fields"
    REPORT = "report"

    def __str__(self) -> str:
        return str(self.value)
