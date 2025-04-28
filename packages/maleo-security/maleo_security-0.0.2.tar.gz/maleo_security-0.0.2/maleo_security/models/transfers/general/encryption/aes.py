from __future__ import annotations
from pydantic import Field
from typing import List
from maleo_security.models.schemas.encryption import MaleoSecurityEncryptionSchemas

class MaleoSecurityAESEncryptionGeneralTransfers:
    class CipherPackage(
        MaleoSecurityEncryptionSchemas.Ciphertext,
        MaleoSecurityEncryptionSchemas.InitializationVector
    ): pass
    
    class PlainPackage(MaleoSecurityEncryptionSchemas.Plaintext): pass

    class SingleEncryption(MaleoSecurityEncryptionSchemas.Key):
        cipher_package:MaleoSecurityAESEncryptionGeneralTransfers.CipherPackage = Field(..., description="Cipher package")

    class MultipleEncryption(MaleoSecurityEncryptionSchemas.Key):
        cipher_packages:List[MaleoSecurityAESEncryptionGeneralTransfers.CipherPackage] = Field(..., description="Cipher packages")

    class SingleDecryption(MaleoSecurityEncryptionSchemas.Key):
        plain_package:MaleoSecurityAESEncryptionGeneralTransfers.PlainPackage = Field(..., description="Plain package")

    class MultipleDecryption(MaleoSecurityEncryptionSchemas.Key):
        plain_packages:List[MaleoSecurityAESEncryptionGeneralTransfers.PlainPackage] = Field(..., description="Plain packages")