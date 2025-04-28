from maleo_foundation.models.transfers.results.service.general import BaseServiceGeneralResultsTransfers
from maleo_security.models.schemas.token import MaleoSecurityTokenSchemas
from maleo_security.models.transfers.general.token import MaleoSecurityTokenGeneralTransfers

class MaleoSecurityTokenResultsTransfers:
    class Fail(BaseServiceGeneralResultsTransfers.Fail): pass

    class Encode(BaseServiceGeneralResultsTransfers.SingleData):
        data:MaleoSecurityTokenSchemas.Token

    class Decode(BaseServiceGeneralResultsTransfers.SingleData):
        data:MaleoSecurityTokenGeneralTransfers.Payload