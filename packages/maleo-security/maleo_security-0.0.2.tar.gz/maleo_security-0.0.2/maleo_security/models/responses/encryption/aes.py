from pydantic import Field
from maleo_foundation.models.responses import BaseResponses
from maleo_security.models.transfers.general.encryption.aes import MaleoSecurityAESEncryptionGeneralTransfers

class MaleoSecurityAESEncryptionResponses:
    class SingleEncryption(BaseResponses.SingleData):
        code:str = "SEC-ENC-AES-001"
        message:str = "Succesfully encrypted single plaintext"
        description:str = "The given plaintext successfully encrypted with AES algorithm"
        data:MaleoSecurityAESEncryptionGeneralTransfers.SingleEncryption = Field(..., description="Single encryption data")

    class MultipleEncryption(BaseResponses.SingleData):
        code:str = "SEC-ENC-AES-002"
        message:str = "Succesfully encrypted multiple plaintexts"
        description:str = "The given plaintexts successfully encrypted with AES algorithm"
        data:MaleoSecurityAESEncryptionGeneralTransfers.MultipleEncryption = Field(..., description="Multiple encryption data")

    class SingleDecryption(BaseResponses.SingleData):
        code:str = "SEC-ENC-AES-003"
        message:str = "Succesfully decrypted single ciphertext"
        description:str = "The given ciphertext successfully decrypted with AES algorithm"
        data:MaleoSecurityAESEncryptionGeneralTransfers.SingleDecryption = Field(..., description="Single decryption data")

    class MultipleDecryption(BaseResponses.SingleData):
        code:str = "SEC-ENC-AES-004"
        message:str = "Succesfully decrypted multiple ciphertexts"
        description:str = "The given ciphertexts successfully decrypted with AES algorithm"
        data:MaleoSecurityAESEncryptionGeneralTransfers.MultipleDecryption = Field(..., description="Multiple decryption data")