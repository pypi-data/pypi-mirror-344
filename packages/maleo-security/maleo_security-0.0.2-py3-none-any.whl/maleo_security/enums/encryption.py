from __future__ import annotations
from enum import StrEnum

class MaleoSecurityEncryptionEnums:
    class EncryptionType(StrEnum):
        AES = "aes"
        RSA = "rsa"