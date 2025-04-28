from typing import Union
from maleo_security.models.transfers.results.encryption.rsa import MaleoSecurityRSAEncryptionResultsTransfers

class MaleoSecurityRSAEncryptionResultsTypes:
    SingleEncryption = Union[
        MaleoSecurityRSAEncryptionResultsTransfers.Fail,
        MaleoSecurityRSAEncryptionResultsTransfers.SingleEncryption
    ]

    MultipleEncryption = Union[
        MaleoSecurityRSAEncryptionResultsTransfers.Fail,
        MaleoSecurityRSAEncryptionResultsTransfers.MultipleEncryption
    ]

    SingleDecryption = Union[
        MaleoSecurityRSAEncryptionResultsTransfers.Fail,
        MaleoSecurityRSAEncryptionResultsTransfers.SingleDecryption
    ]

    MultipleDecryption = Union[
        MaleoSecurityRSAEncryptionResultsTransfers.Fail,
        MaleoSecurityRSAEncryptionResultsTransfers.MultipleDecryption
    ]