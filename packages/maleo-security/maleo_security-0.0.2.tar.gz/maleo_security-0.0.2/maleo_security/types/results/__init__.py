from __future__ import annotations
from .key import MaleoSecurityKeyResultsTypes
from .hash import MaleoSecurityHashResultsTypes
from .encryption import MaleoSecurityEncryptionResultsTypes
from .signature import MaleoSecuritySignatureResultsTypes
from .token import MaleoSecurityTokenResultsTypes
from .secret import MaleoSecuritySecretResultsTypes

class MaleoSecurityResultsTypes:
    Key = MaleoSecurityKeyResultsTypes
    Hash = MaleoSecurityHashResultsTypes
    Encryption = MaleoSecurityEncryptionResultsTypes
    Signature = MaleoSecuritySignatureResultsTypes
    Token = MaleoSecurityTokenResultsTypes
    Secret = MaleoSecuritySecretResultsTypes