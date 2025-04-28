from __future__ import annotations
from .aes import MaleoSecurityAESEncryptionClientService
from .rsa import MaleoSecurityRSAEncryptionClientService

class MaleoSecurityEncryptionClientService:
    AES = MaleoSecurityAESEncryptionClientService
    RSA = MaleoSecurityRSAEncryptionClientService