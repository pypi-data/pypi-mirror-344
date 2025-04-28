from __future__ import annotations
from enum import StrEnum

class MaleoSecurityKeyEnums:
    class KeyType(StrEnum):
        PRIVATE = "private"
        PUBLIC = "public"