from pydantic import Field
from typing import List
from maleo_security.models.schemas.encryption import MaleoSecurityEncryptionSchemas
from maleo_security.models.transfers.general.encryption.aes import MaleoSecurityAESEncryptionGeneralTransfers

class MaleoSecurityAESEncryptionParametersTransfers:
    class EncryptSingle(MaleoSecurityEncryptionSchemas.Plaintext): pass

    class EncryptMultiple(MaleoSecurityEncryptionSchemas.ListOfPlaintext): pass

    class DecryptSingle(MaleoSecurityEncryptionSchemas.Key):
        cipher_package:MaleoSecurityAESEncryptionGeneralTransfers.CipherPackage = Field(..., description="Cipher package")

    class DecryptMultiple(MaleoSecurityEncryptionSchemas.Key):
        cipher_packages:List[MaleoSecurityAESEncryptionGeneralTransfers.CipherPackage] = Field(..., description="Cipher packages")