from pydantic import Field
from typing import List
from maleo_foundation.models.responses import BaseResponses
from maleo_security.models.schemas.signature import MaleoSecuritySignatureSchemas

class MaleoSecuritySignatureResponses:
    class SingleSignature(BaseResponses.SingleData):
        code:str = "SEC-SGN-001"
        message:str = "Succesfully created signature"
        description:str = "A new signature successfully created for the given message"
        data:MaleoSecuritySignatureSchemas.Signature = Field(..., description="Single signature data")

    class MultipleSignature(BaseResponses.UnpaginatedMultipleData):
        code:str = "SEC-SGN-002"
        message:str = "Succesfully created signatures"
        description:str = "Multiple signatures successfully created for the given messages"
        data:List[MaleoSecuritySignatureSchemas.Signature] = Field(..., description="Multiple signature data")

    class SingleVerify(BaseResponses.SingleData):
        code:str = "SEC-SGN-001"
        message:str = "Successfully verified signature"
        description:str = "The signature successfully verified for the given message"
        data:MaleoSecuritySignatureSchemas.IsValid = Field(..., description="Single verify data")

    class MultipleVerify(BaseResponses.UnpaginatedMultipleData):
        code:str = "SEC-SGN-002"
        message:str = "Successfully verified signatures"
        description:str = "Multiple signatures successfully verified for the given messages"
        data:List[MaleoSecuritySignatureSchemas.IsValid] = Field(..., description="Multiple verify data")