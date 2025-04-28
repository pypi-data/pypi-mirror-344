from __future__ import annotations
from .aes import MaleoSecurityAESEncryptionResultsTypes
from .rsa import MaleoSecurityRSAEncryptionResultsTypes

class MaleoSecurityEncryptionResultsTypes:
    AES = MaleoSecurityAESEncryptionResultsTypes
    RSA = MaleoSecurityRSAEncryptionResultsTypes