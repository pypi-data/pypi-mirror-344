from typing import Union
from maleo_security.models.transfers.results.secret import MaleoSecuritySecretResultsTransfers

class MaleoSecuritySecretResultsTypes:
    Base = Union[
        MaleoSecuritySecretResultsTransfers.Fail,
        MaleoSecuritySecretResultsTransfers.NoData,
        MaleoSecuritySecretResultsTransfers.SingleData
    ]