from enum import Enum


class CustomColumnType(str, Enum):
    APPLY_PROMPT = "apply_prompt"
    DATA_LOOKUP = "data_lookup"
    VALIDATED_PROMPT = "validated_prompt"

    def __str__(self) -> str:
        return str(self.value)
