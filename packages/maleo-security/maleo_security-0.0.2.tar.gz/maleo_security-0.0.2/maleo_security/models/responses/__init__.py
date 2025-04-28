from __future__ import annotations
from .key import MaleoSecurityKeyResponses
from .hash import MaleoSecurityHashResponses
from .encryption import MaleoSecurityEncryptionResponses
from .signature import MaleoSecuritySignatureResponses
from .token import MaleoSecurityTokenResponses
from .secret import MaleoSecuritySecretResponses

class MaleoSecurityResponses:
    Key = MaleoSecurityKeyResponses
    Hash = MaleoSecurityHashResponses
    Encryption = MaleoSecurityEncryptionResponses
    Signature = MaleoSecuritySignatureResponses
    Token = MaleoSecurityTokenResponses
    Secret = MaleoSecuritySecretResponses