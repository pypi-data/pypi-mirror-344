from typing import Union
from maleo_security.models.transfers.results.hash import MaleoSecurityHashResultsTransfers

class MaleoSecurityHashResultsTypes:
    Hash = Union[
        MaleoSecurityHashResultsTransfers.Fail,
        MaleoSecurityHashResultsTransfers.Hash
    ]

    Verify = Union[
        MaleoSecurityHashResultsTransfers.Fail,
        MaleoSecurityHashResultsTransfers.Verify
    ]