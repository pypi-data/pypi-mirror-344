from typing import Union
from maleo_security.models.transfers.results.encryption.aes import MaleoSecurityAESEncryptionResultsTransfers

class MaleoSecurityAESEncryptionResultsTypes:
    SingleEncryption = Union[
        MaleoSecurityAESEncryptionResultsTransfers.Fail,
        MaleoSecurityAESEncryptionResultsTransfers.SingleEncryption
    ]

    MultipleEncryption = Union[
        MaleoSecurityAESEncryptionResultsTransfers.Fail,
        MaleoSecurityAESEncryptionResultsTransfers.MultipleEncryption
    ]

    SingleDecryption = Union[
        MaleoSecurityAESEncryptionResultsTransfers.Fail,
        MaleoSecurityAESEncryptionResultsTransfers.SingleDecryption
    ]

    MultipleDecryption = Union[
        MaleoSecurityAESEncryptionResultsTransfers.Fail,
        MaleoSecurityAESEncryptionResultsTransfers.MultipleDecryption
    ]