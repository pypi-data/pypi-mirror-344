from maleo_security.models.schemas.hash import MaleoSecurityHashSchemas

class MaleoSecurityHMACHashParametersTransfers:
    class Hash(
        MaleoSecurityHashSchemas.Message,
        MaleoSecurityHashSchemas.Key
    ): pass

    class Verify(
        MaleoSecurityHashSchemas.Hash,
        MaleoSecurityHashSchemas.Message,
        MaleoSecurityHashSchemas.Key
    ): pass