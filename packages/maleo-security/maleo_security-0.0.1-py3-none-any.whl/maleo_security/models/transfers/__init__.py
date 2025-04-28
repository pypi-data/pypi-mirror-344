from __future__ import annotations
from .general import MaleoSecurityGeneralTransfers
from .parameters import MaleoSecurityParametersTransfers
from .results import MaleoSecurityResultsTransfers

class MaleoSecurityTransfers:
    General = MaleoSecurityGeneralTransfers
    Parameters = MaleoSecurityParametersTransfers
    Results = MaleoSecurityResultsTransfers