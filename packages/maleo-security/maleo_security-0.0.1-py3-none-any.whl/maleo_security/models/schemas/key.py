from __future__ import annotations
from pydantic import BaseModel, Field
from maleo_security.enums.key import MaleoSecurityKeyEnums

class MaleoSecurityKeySchemas:
    class KeySize(BaseModel):
        key_size:int = Field(2048, ge=2048, le=16384, description="Key's size")

    class Key(BaseModel):
        type:MaleoSecurityKeyEnums.KeyType = Field(..., description="Key's type")
        value:str = Field(..., description="Key's value")