from maleo_security.models.schemas.hash import MaleoSecurityHashSchemas

class MaleoSecurityBcryptHashParametersTransfers:
    class Hash(MaleoSecurityHashSchemas.Message): pass

    class Verify(
        MaleoSecurityHashSchemas.Hash,
        MaleoSecurityHashSchemas.Message
    ): pass