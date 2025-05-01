from enum import Enum


class TrendExecutor(str, Enum):
    LLM = "llm"
    SERP = "serp"

    def __str__(self) -> str:
        return str(self.value)
