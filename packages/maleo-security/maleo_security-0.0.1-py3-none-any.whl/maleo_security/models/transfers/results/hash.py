from __future__ import annotations
from pydantic import Field
from maleo_foundation.models.transfers.results.service.general import BaseServiceGeneralResultsTransfers
from maleo_security.models.transfers.general.hash import MaleoSecurityHashGeneralTransfers

class MaleoSecurityHashResultsTransfers:
    class Fail(BaseServiceGeneralResultsTransfers.Fail): pass

    class Hash(BaseServiceGeneralResultsTransfers.SingleData):
        data:MaleoSecurityHashGeneralTransfers.Hash = Field(..., description="Hash data")

    class Verify(BaseServiceGeneralResultsTransfers.SingleData):
        data:MaleoSecurityHashGeneralTransfers.Verify = Field(..., description="Verify data")