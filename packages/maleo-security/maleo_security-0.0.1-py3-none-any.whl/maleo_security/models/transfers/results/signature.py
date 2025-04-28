from pydantic import Field
from typing import List
from maleo_foundation.models.transfers.results.service.general import BaseServiceGeneralResultsTransfers
from maleo_security.models.schemas.signature import MaleoSecuritySignatureSchemas

class MaleoSecuritySignatureResultsTransfers:
    class Fail(BaseServiceGeneralResultsTransfers.Fail): pass

    class SingleSignature(BaseServiceGeneralResultsTransfers.SingleData):
        data:MaleoSecuritySignatureSchemas.Signature = Field(..., description="Single signature data")

    class MultipleSignature(BaseServiceGeneralResultsTransfers.UnpaginatedMultipleData):
        data:List[MaleoSecuritySignatureSchemas.Signature] = Field(..., description="Multiple signature data")

    class SingleVerify(BaseServiceGeneralResultsTransfers.SingleData):
        data:MaleoSecuritySignatureSchemas.IsValid = Field(..., description="Single verify data")

    class MultipleVerify(BaseServiceGeneralResultsTransfers.UnpaginatedMultipleData):
        data:List[MaleoSecuritySignatureSchemas.IsValid] = Field(..., description="Multiple verify data")