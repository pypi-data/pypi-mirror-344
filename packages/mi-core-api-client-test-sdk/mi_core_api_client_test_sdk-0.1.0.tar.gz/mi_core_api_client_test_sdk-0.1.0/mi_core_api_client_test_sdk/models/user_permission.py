from enum import Enum


class UserPermission(str, Enum):
    GATEWAY_ACCESS = "GATEWAY_ACCESS"
    ZG_API_ACCESS = "ZG_API_ACCESS"

    def __str__(self) -> str:
        return str(self.value)
