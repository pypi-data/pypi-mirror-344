from pydantic import Field
from maleo_foundation.models.transfers.results.service.general import BaseServiceGeneralResultsTransfers
from maleo_security.models.transfers.general.encryption.aes import MaleoSecurityAESEncryptionGeneralTransfers

class MaleoSecurityAESEncryptionResultsTransfers:
    class Fail(BaseServiceGeneralResultsTransfers.Fail): pass

    class SingleEncryption(BaseServiceGeneralResultsTransfers.SingleData):
        data:MaleoSecurityAESEncryptionGeneralTransfers.SingleEncryption = Field(..., description="Single encryption data")

    class MultipleEncryption(BaseServiceGeneralResultsTransfers.SingleData):
        data:MaleoSecurityAESEncryptionGeneralTransfers.MultipleEncryption = Field(..., description="Multiple encryption data")

    class SingleDecryption(BaseServiceGeneralResultsTransfers.SingleData):
        data:MaleoSecurityAESEncryptionGeneralTransfers.SingleDecryption = Field(..., description="Single decryption data")

    class MultipleDecryption(BaseServiceGeneralResultsTransfers.SingleData):
        data:MaleoSecurityAESEncryptionGeneralTransfers.MultipleDecryption = Field(..., description="Multiple decryption data")