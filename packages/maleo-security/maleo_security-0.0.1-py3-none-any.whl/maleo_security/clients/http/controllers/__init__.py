from __future__ import annotations
from .key import MaleoSecurityKeyHTTPClientController
from .hash import MaleoSecurityHashHTTPClientController
from .encryption import MaleoSecurityEncryptionHTTPClientController
from .signature import MaleoSecuritySignatureHTTPClientController
from .token import MaleoSecurityTokenHTTPClientController

class MaleoSecurityHTTPClientControllers:
    Key = MaleoSecurityKeyHTTPClientController
    Hash = MaleoSecurityHashHTTPClientController
    Encryption = MaleoSecurityEncryptionHTTPClientController
    Signature = MaleoSecuritySignatureHTTPClientController
    Token = MaleoSecurityTokenHTTPClientController