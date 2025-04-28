from pydantic import Field
from maleo_foundation.models.responses import BaseResponses
from maleo_security.models.transfers.general.hash import MaleoSecurityHashGeneralTransfers

class MaleoSecurityHashResponses:
    class HashSuccess(BaseResponses.SingleData):
        code:str = "SEC-HSH-001"
        message:str = "Successfully created hash"
        description:str = "A new hash successfully created for the given message"
        data:MaleoSecurityHashGeneralTransfers.Hash = Field(..., description="Hash data")

    class VerifySuccess(BaseResponses.SingleData):
        code:str = "SEC-HSH-002"
        message:str = "Successfully verified hash"
        description:str = "The hash successfully verified for the given message"
        data:MaleoSecurityHashGeneralTransfers.Verify = Field(..., description="Verify data")