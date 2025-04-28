from pydantic import BaseModel, Field
from maleo_foundation.types import BaseTypes

class MaleoSecurityEncryptionSchemas:
    class Key(BaseModel):
        key:str = Field(..., description="Key")

    class InitializationVector(BaseModel):
        initialization_vector:str = Field(..., description="Initialization vector")

    class Plaintext(BaseModel):
        plaintext:str = Field(..., description="Plaintext")

    class ListOfPlaintext(BaseModel):
        plaintexts:BaseTypes.ListOfStrings = Field(..., description="Plaintexts")

    class Ciphertext(BaseModel):
        ciphertext:str = Field(..., description="Ciphertext")

    class ListOfCiphertext(BaseModel):
        ciphertexts:BaseTypes.ListOfStrings = Field(..., description="Ciphertexts")

    class CipherPackage(Ciphertext, InitializationVector): pass