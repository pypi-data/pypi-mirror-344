from __future__ import annotations
from pydantic import Field
from maleo_foundation.models.transfers.results.service.general import BaseServiceGeneralResultsTransfers
from maleo_security.models.transfers.general.key import MaleoSecurityKeyGeneralTransfers

class MaleoSecurityKeyResultsTransfers:
    class Fail(BaseServiceGeneralResultsTransfers.Fail): pass

    class SinglePrivate(BaseServiceGeneralResultsTransfers.SingleData):
        data:MaleoSecurityKeyGeneralTransfers.PrivateKey = Field(..., description="Private key data")

    class SinglePublic(BaseServiceGeneralResultsTransfers.SingleData):
        data:MaleoSecurityKeyGeneralTransfers.PublicKey = Field(..., description="Private key data")

    class SinglePair(BaseServiceGeneralResultsTransfers.SingleData):
        data:MaleoSecurityKeyGeneralTransfers.KeyPair = Field(..., description="Key pair data")