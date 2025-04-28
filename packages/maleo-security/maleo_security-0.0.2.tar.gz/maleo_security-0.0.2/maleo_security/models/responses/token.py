from pydantic import Field
from maleo_foundation.models.responses import BaseResponses
from maleo_security.models.schemas.token import MaleoSecurityTokenSchemas
from maleo_security.models.transfers.general.token import MaleoSecurityTokenGeneralTransfers

class MaleoSecurityTokenResponses:
    class Encode(BaseResponses.SingleData):
        code:str = "SEC-TKN-001"
        message:str = "Succesfully encoded given payload"
        description:str = "The payload is encoded with data provided on request"
        data:MaleoSecurityTokenSchemas.Token = Field(..., description="Token data")

    class Decode(BaseResponses.SingleData):
        code:str = "SEC-TKN-002"
        message:str = "Succesfully decoded given token"
        description:str = "The token is decoded with data provided on request"
        data:MaleoSecurityTokenGeneralTransfers.Payload = Field(..., description="Payload data")