from __future__ import annotations
from .aes import MaleoSecurityAESEncryptionGeneralTransfers
from .rsa import MaleoSecurityRSAEncryptionGeneralTransfers

class MaleoSecurityEncryptionGeneralTransfers:
    AES = MaleoSecurityAESEncryptionGeneralTransfers
    RSA = MaleoSecurityRSAEncryptionGeneralTransfers