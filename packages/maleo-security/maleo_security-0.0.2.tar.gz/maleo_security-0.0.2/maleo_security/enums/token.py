from __future__ import annotations
from enum import StrEnum

class MaleoSecurityTokenEnums:
    class TokenType(StrEnum):
        REFRESH = "refresh"
        ACCESS = "access"