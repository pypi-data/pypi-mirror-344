from __future__ import annotations
from pydantic import BaseModel, Field
from maleo_security.enums.key import MaleoSecurityKeyEnums
from maleo_security.models.schemas.key import MaleoSecurityKeySchemas

class MaleoSecurityKeyGeneralTransfers:
    class PrivateKey(MaleoSecurityKeySchemas.Key):
        type:MaleoSecurityKeyEnums.KeyType = Field(MaleoSecurityKeyEnums.KeyType.PRIVATE, description="Private key's type")

    class PublicKey(MaleoSecurityKeySchemas.Key):
        type:MaleoSecurityKeyEnums.KeyType = Field(MaleoSecurityKeyEnums.KeyType.PUBLIC, description="Public key's type")

    class KeyPair(BaseModel):
        private:MaleoSecurityKeyGeneralTransfers.PrivateKey = Field(..., description="Private key's data")
        public:MaleoSecurityKeyGeneralTransfers.PublicKey = Field(..., description="Public key's data")