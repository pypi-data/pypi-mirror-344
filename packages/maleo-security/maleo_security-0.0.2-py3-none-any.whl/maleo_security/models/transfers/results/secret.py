from maleo_foundation.models.transfers.results.service.general import BaseServiceGeneralResultsTransfers
from maleo_security.models.transfers.general.secret import MaleoSecuritySecretGeneralTransfers

class MaleoSecuritySecretResultsTransfers:
    class Fail(BaseServiceGeneralResultsTransfers.Fail): pass

    class NoData(BaseServiceGeneralResultsTransfers.NoData): pass

    class SingleData(BaseServiceGeneralResultsTransfers.SingleData):
        data:MaleoSecuritySecretGeneralTransfers.Base