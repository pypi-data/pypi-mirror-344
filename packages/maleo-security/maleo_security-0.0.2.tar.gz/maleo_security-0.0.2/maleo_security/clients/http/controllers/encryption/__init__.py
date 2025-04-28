from __future__ import annotations
from .aes import MaleoSecurityAESEncryptionHTTPClientController
from .rsa import MaleoSecurityRSAEncryptionHTTPClientController

class MaleoSecurityEncryptionHTTPClientController:
    AES = MaleoSecurityAESEncryptionHTTPClientController
    RSA = MaleoSecurityRSAEncryptionHTTPClientController