from __future__ import annotations
from enum import StrEnum

class MaleoSecurityHashEnums:
    class HashType(StrEnum):
        BCRYPT = "bcrypt"
        HMAC = "hmac"
        SHA256 = "sha256"