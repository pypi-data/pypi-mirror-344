from __future__ import annotations
from .key import MaleoSecurityKeyClientService
from .hash import MaleoSecurityHashClientService
from .encryption import MaleoSecurityEncryptionClientService
from .signature import MaleoSecuritySignatureClientService
from .token import MaleoSecurityTokenClientService

class MaleoSecurityClientServices:
    Key = MaleoSecurityKeyClientService
    Hash = MaleoSecurityHashClientService
    Encryption = MaleoSecurityEncryptionClientService
    Signature = MaleoSecuritySignatureClientService
    Token = MaleoSecurityTokenClientService