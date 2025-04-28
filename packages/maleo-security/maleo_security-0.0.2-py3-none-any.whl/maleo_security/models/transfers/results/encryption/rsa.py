from pydantic import Field
from maleo_foundation.models.transfers.results.service.general import BaseServiceGeneralResultsTransfers
from maleo_security.models.transfers.general.encryption.rsa import MaleoSecurityRSAEncryptionGeneralTransfers

class MaleoSecurityRSAEncryptionResultsTransfers:
    class Fail(BaseServiceGeneralResultsTransfers.Fail): pass

    class SingleEncryption(BaseServiceGeneralResultsTransfers.SingleData):
        data:MaleoSecurityRSAEncryptionGeneralTransfers.SingleEncryption = Field(..., description="Single encryption data")

    class MultipleEncryption(BaseServiceGeneralResultsTransfers.SingleData):
        data:MaleoSecurityRSAEncryptionGeneralTransfers.MultipleEncryption = Field(..., description="Multiple encryption data")

    class SingleDecryption(BaseServiceGeneralResultsTransfers.SingleData):
        data:MaleoSecurityRSAEncryptionGeneralTransfers.SingleDecryption = Field(..., description="Single decryption data")

    class MultipleDecryption(BaseServiceGeneralResultsTransfers.SingleData):
        data:MaleoSecurityRSAEncryptionGeneralTransfers.MultipleDecryption = Field(..., description="Multiple decryption data")