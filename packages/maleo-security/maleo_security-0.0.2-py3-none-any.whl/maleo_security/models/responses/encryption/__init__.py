from __future__ import annotations
from .aes import MaleoSecurityAESEncryptionResponses
from .rsa import MaleoSecurityRSAEncryptionResponses

class MaleoSecurityEncryptionResponses:
    AES = MaleoSecurityAESEncryptionResponses
    RSA = MaleoSecurityRSAEncryptionResponses