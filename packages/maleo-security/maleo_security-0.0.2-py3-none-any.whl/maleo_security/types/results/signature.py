from typing import Union
from maleo_security.models.transfers.results.signature import MaleoSecuritySignatureResultsTransfers

class MaleoSecuritySignatureResultsTypes:
    SingleSignature = Union[
        MaleoSecuritySignatureResultsTransfers.Fail,
        MaleoSecuritySignatureResultsTransfers.SingleSignature
    ]

    MultipleSignature = Union[
        MaleoSecuritySignatureResultsTransfers.Fail,
        MaleoSecuritySignatureResultsTransfers.MultipleSignature
    ]

    SingleVerify = Union[
        MaleoSecuritySignatureResultsTransfers.Fail,
        MaleoSecuritySignatureResultsTransfers.SingleVerify
    ]

    MultipleVerify = Union[
        MaleoSecuritySignatureResultsTransfers.Fail,
        MaleoSecuritySignatureResultsTransfers.MultipleVerify
    ]