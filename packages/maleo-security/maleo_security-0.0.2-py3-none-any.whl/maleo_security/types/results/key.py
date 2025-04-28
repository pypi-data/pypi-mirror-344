from typing import Union
from maleo_security.models.transfers.results.key import MaleoSecurityKeyResultsTransfers

class MaleoSecurityKeyResultsTypes:
    CreatePrivate = Union[
        MaleoSecurityKeyResultsTransfers.Fail,
        MaleoSecurityKeyResultsTransfers.SinglePrivate
    ]

    CreatePublic = Union[
        MaleoSecurityKeyResultsTransfers.Fail,
        MaleoSecurityKeyResultsTransfers.SinglePublic
    ]

    CreatePair = Union[
        MaleoSecurityKeyResultsTransfers.Fail,
        MaleoSecurityKeyResultsTransfers.SinglePair
    ]