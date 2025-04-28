from maleo_security.models.schemas.token import MaleoSecurityTokenSchemas
from maleo_security.models.transfers.general.token import MaleoSecurityTokenGeneralTransfers

class MaleoSecurityTokenParametersTransfers:
    class Encode(
        MaleoSecurityTokenGeneralTransfers.Payload,
        MaleoSecurityTokenSchemas.Key
    ): pass

    class Decode(
        MaleoSecurityTokenSchemas.Token,
        MaleoSecurityTokenSchemas.Key
    ): pass