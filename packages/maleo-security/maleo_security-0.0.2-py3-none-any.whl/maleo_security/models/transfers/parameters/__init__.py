from __future__ import annotations
from .key import MaleoSecurityKeyParametersTransfers
from .hash import MaleoSecurityHashParametersTransfers
from .encryption import MaleoSecurityEncryptionParametersTransfers
from .signature import MaleoSecuritySignatureParametersTransfers
from .token import MaleoSecurityTokenParametersTransfers

class MaleoSecurityParametersTransfers:
    Key = MaleoSecurityKeyParametersTransfers
    Hash = MaleoSecurityHashParametersTransfers
    Encryption = MaleoSecurityEncryptionParametersTransfers
    Signature = MaleoSecuritySignatureParametersTransfers
    Token = MaleoSecurityTokenParametersTransfers