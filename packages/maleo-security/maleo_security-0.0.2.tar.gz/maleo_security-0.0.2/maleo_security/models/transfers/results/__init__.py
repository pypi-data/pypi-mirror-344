from __future__ import annotations
from .key import MaleoSecurityKeyResultsTransfers
from .hash import MaleoSecurityHashResultsTransfers
from .encryption import MaleoSecurityEncryptionResultsTransfers
from .signature import MaleoSecuritySignatureResultsTransfers
from .token import MaleoSecurityTokenResultsTransfers
from .secret import MaleoSecuritySecretResultsTransfers

class MaleoSecurityResultsTransfers:
    Key = MaleoSecurityKeyResultsTransfers
    Hash = MaleoSecurityHashResultsTransfers
    Encryption = MaleoSecurityEncryptionResultsTransfers
    Signature = MaleoSecuritySignatureResultsTransfers
    Token = MaleoSecurityTokenResultsTransfers
    Secret = MaleoSecuritySecretResultsTransfers