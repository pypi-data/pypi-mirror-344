from enum import Enum


class ReportType(str, Enum):
    APPLY_LLM = "apply_llm"
    CLUSTER_TOPICS = "cluster_topics"
    EXTRACT_ENTITIES = "extract_entities"
    SUMMARIZE = "summarize"

    def __str__(self) -> str:
        return str(self.value)
