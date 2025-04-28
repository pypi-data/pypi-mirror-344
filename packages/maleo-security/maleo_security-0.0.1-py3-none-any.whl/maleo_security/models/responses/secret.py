from pydantic import Field
from maleo_foundation.models.responses import BaseResponses
from maleo_security.models.schemas.secret import MaleoSecuritySecretSchemas
from maleo_security.models.transfers.general.secret import MaleoSecuritySecretGeneralTransfers

class MaleoSecuritySecretResponses:
    class Get(BaseResponses.SingleData):
        code:str = "SEC-SCR-001"
        message:str = "Secret found"
        description:str = "Requested secret found in database"
        data:MaleoSecuritySecretGeneralTransfers.Base = Field(..., description="Secret data")

    class Create(BaseResponses.SingleData):
        code:str = "SEC-SCR-002"
        message:str = "Succesfully created new secret"
        description:str = "A new secret is created with data provided on request"
        data:MaleoSecuritySecretGeneralTransfers.Base = Field(..., description="Payload data")