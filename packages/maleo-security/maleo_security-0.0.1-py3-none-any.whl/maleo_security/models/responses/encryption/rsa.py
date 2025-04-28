from pydantic import Field
from maleo_foundation.models.responses import BaseResponses
from maleo_security.models.transfers.results.encryption.rsa import MaleoSecurityRSAEncryptionGeneralTransfers

class MaleoSecurityRSAEncryptionResponses:
    class SingleEncryption(BaseResponses.SingleData):
        code:str = "SEC-ENC-RSA-001"
        message:str = "Succesfully encrypted single plaintext"
        description:str = "The given plaintext successfully encrypted with RSA algorithm"
        data:MaleoSecurityRSAEncryptionGeneralTransfers.SingleEncryption = Field(..., description="Single encryption data")

    class MultipleEncryption(BaseResponses.SingleData):
        code:str = "SEC-ENC-RSA-002"
        message:str = "Succesfully encrypted multiple plaintexts"
        description:str = "The given plaintexts successfully encrypted with RSA algorithm"
        data:MaleoSecurityRSAEncryptionGeneralTransfers.MultipleEncryption = Field(..., description="Multiple encryption data")

    class SingleDecryption(BaseResponses.SingleData):
        code:str = "SEC-ENC-RSA-003"
        message:str = "Succesfully decrypted single ciphertext"
        description:str = "The given ciphertext successfully decrypted with RSA algorithm"
        data:MaleoSecurityRSAEncryptionGeneralTransfers.SingleDecryption = Field(..., description="Single decryption data")

    class MultipleDecryption(BaseResponses.SingleData):
        code:str = "SEC-ENC-RSA-004"
        message:str = "Succesfully decrypted multiple ciphertexts"
        description:str = "The given ciphertexts successfully decrypted with RSA algorithm"
        data:MaleoSecurityRSAEncryptionGeneralTransfers.MultipleDecryption = Field(..., description="Multiple decryption data")