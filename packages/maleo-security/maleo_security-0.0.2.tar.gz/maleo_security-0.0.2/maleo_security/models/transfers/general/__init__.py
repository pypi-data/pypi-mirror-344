from __future__ import annotations
from .key import MaleoSecurityKeyGeneralTransfers
from .hash import MaleoSecurityHashGeneralTransfers
from .encryption import MaleoSecurityEncryptionGeneralTransfers
from .signature import MaleoSecuritySignatureGeneralTransfers
from .token import MaleoSecurityTokenGeneralTransfers
from .secret import MaleoSecuritySecretGeneralTransfers

class MaleoSecurityGeneralTransfers:
    Key = MaleoSecurityKeyGeneralTransfers
    Hash = MaleoSecurityHashGeneralTransfers
    Encryption = MaleoSecurityEncryptionGeneralTransfers
    Signature = MaleoSecuritySignatureGeneralTransfers
    Token = MaleoSecurityTokenGeneralTransfers
    Secret = MaleoSecuritySecretGeneralTransfers