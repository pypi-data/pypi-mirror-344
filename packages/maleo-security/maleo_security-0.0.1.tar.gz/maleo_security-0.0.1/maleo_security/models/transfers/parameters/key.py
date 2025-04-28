from maleo_security.models.schemas.key import MaleoSecurityKeySchemas
from maleo_security.models.transfers.general.key import MaleoSecurityKeyGeneralTransfers

class MaleoSecurityKeyParametersTransfers:
    class CreatePrivateOrPair(MaleoSecurityKeySchemas.KeySize): pass
    class CreatePublic(MaleoSecurityKeyGeneralTransfers.PrivateKey): pass