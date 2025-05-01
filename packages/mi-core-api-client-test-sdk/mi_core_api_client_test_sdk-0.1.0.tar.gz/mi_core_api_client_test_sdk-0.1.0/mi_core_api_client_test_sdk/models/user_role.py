from enum import Enum


class UserRole(str, Enum):
    MODERATOR = "moderator"
    SUPERUSER = "superuser"
    USER = "user"

    def __str__(self) -> str:
        return str(self.value)
