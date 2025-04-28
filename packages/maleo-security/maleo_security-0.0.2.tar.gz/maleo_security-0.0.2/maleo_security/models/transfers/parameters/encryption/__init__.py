from __future__ import annotations
from .aes import MaleoSecurityAESEncryptionParametersTransfers
from .rsa import MaleoSecurityRSAEncryptionParametersTransfers

class MaleoSecurityEncryptionParametersTransfers:
    AES = MaleoSecurityAESEncryptionParametersTransfers
    RSA = MaleoSecurityRSAEncryptionParametersTransfers