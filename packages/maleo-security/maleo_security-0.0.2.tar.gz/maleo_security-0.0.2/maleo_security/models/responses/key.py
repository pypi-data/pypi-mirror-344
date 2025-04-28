from pydantic import Field
from maleo_foundation.models.responses import BaseResponses
from maleo_security.models.transfers.general.key import MaleoSecurityKeyGeneralTransfers

class MaleoSecurityKeyResponses:
    class CreatePrivateSuccess(BaseResponses.SingleData):
        code:str = "SEC-KEY-001"
        message:str = "Successfully created private key"
        description:str = "A new private key successfully created by the given parameters"
        data:MaleoSecurityKeyGeneralTransfers.PrivateKey = Field(..., description="Private key data")

    class CreatePublicSuccess(BaseResponses.SingleData):
        code:str = "SEC-KEY-002"
        message:str = "Successfully created public key"
        description:str = "A new public key successfully created by the given parameters"
        data:MaleoSecurityKeyGeneralTransfers.PublicKey = Field(..., description="Public key data")

    class CreatePairSuccess(BaseResponses.SingleData):
        code:str = "SEC-KEY-003"
        message:str = "Successfully created key pair"
        description:str = "A new key pair successfully created by the given parameters"
        data:MaleoSecurityKeyGeneralTransfers.KeyPair = Field(..., description="Key pair data")