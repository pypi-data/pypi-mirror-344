from __future__ import annotations
from .general import MaleoSecurityGeneralEnums
from .key import MaleoSecurityKeyEnums
from .hash import MaleoSecurityHashEnums
from .encryption import MaleoSecurityEncryptionEnums
from .token import MaleoSecurityTokenEnums

class MaleoSecurityEnums:
    General = MaleoSecurityGeneralEnums
    Key = MaleoSecurityKeyEnums
    Hash = MaleoSecurityHashEnums
    Encryption = MaleoSecurityEncryptionEnums
    Token = MaleoSecurityTokenEnums