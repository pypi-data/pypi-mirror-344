from pydantic import BaseModel, Field
from maleo_foundation.types import BaseTypes

class MaleoSecuritySignatureSchemas:
    class Key(BaseModel):
        key:str = Field(..., description="Key")

    class Message(BaseModel):
        message:str = Field(..., description="Message")

    class ListOfMessage(BaseModel):
        messages:BaseTypes.ListOfStrings = Field(..., description="Messages")

    class Signature(BaseModel):
        signature:str = Field(..., description="Signature")

    class ListOfSignature(BaseModel):
        signatures:BaseTypes.ListOfStrings = Field(..., description="Signatures")

    class IsValid(BaseModel):
        is_valid:bool = Field(..., description="Is valid signature")

    class ListOfIsValid(BaseModel):
        is_valids:BaseTypes.ListOfBools = Field(..., description="Is valid signatures")