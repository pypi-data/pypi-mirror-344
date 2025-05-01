from enum import Enum


class SubredditsSortBy(str, Enum):
    MEMBERS = "members"
    NONE = "none"
    ONLINE_MEMBERS = "online_members"

    def __str__(self) -> str:
        return str(self.value)
