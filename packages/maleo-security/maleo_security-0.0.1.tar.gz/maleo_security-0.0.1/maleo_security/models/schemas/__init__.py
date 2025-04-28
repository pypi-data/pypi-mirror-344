from __future__ import annotations
from .key import MaleoSecurityKeySchemas
from .hash import MaleoSecurityHashSchemas
from .encryption import MaleoSecurityEncryptionSchemas
from .signature import MaleoSecuritySignatureSchemas
from .token import MaleoSecurityTokenSchemas
from .secret import MaleoSecuritySecretSchemas

class MaleoSecuritySchemas:
    Key = MaleoSecurityKeySchemas
    Hash = MaleoSecurityHashSchemas
    Encryption = MaleoSecurityEncryptionSchemas
    Signature = MaleoSecuritySignatureSchemas
    Token = MaleoSecurityTokenSchemas
    Secret = MaleoSecuritySecretSchemas