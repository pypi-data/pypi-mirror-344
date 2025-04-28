from typing import Union
from maleo_security.models.transfers.results.token import MaleoSecurityTokenResultsTransfers

class MaleoSecurityTokenResultsTypes:
    Encode = Union[
        MaleoSecurityTokenResultsTransfers.Fail,
        MaleoSecurityTokenResultsTransfers.Encode
    ]

    Decode = Union[
        MaleoSecurityTokenResultsTransfers.Fail,
        MaleoSecurityTokenResultsTransfers.Decode
    ]