from pydantic import Field
from typing import List
from maleo_security.models.schemas.signature import MaleoSecuritySignatureSchemas
from maleo_security.models.transfers.general.signature import MaleoSecuritySignatureGeneralTransfers

class MaleoSecuritySignatureParametersTransfers:
    class SignSingle(
        MaleoSecuritySignatureSchemas.Message,
        MaleoSecuritySignatureSchemas.Key
    ): pass

    class SignMultiple(
        MaleoSecuritySignatureSchemas.ListOfMessage,
        MaleoSecuritySignatureSchemas.Key
    ): pass

    class VerifySingle(MaleoSecuritySignatureSchemas.Key):
        signature_package:MaleoSecuritySignatureGeneralTransfers.SignaturePackage = Field(..., description="Signature package")

    class VerifyMultiple(MaleoSecuritySignatureSchemas.Key):
        signature_packages:List[MaleoSecuritySignatureGeneralTransfers.SignaturePackage] = Field(..., description="Signature packages")