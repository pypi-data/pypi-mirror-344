from __future__ import annotations
from maleo_security.models.schemas.signature import MaleoSecuritySignatureSchemas

class MaleoSecuritySignatureGeneralTransfers:
    class SignaturePackage(
        MaleoSecuritySignatureSchemas.Message,
        MaleoSecuritySignatureSchemas.Signature
    ): pass