from __future__ import annotations
from .aes import MaleoSecurityAESEncryptionResultsTransfers
from .rsa import MaleoSecurityRSAEncryptionResultsTransfers

class MaleoSecurityEncryptionResultsTransfers:
    AES = MaleoSecurityAESEncryptionResultsTransfers
    RSA = MaleoSecurityRSAEncryptionResultsTransfers