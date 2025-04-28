from maleo_security.models.schemas.secret import MaleoSecuritySecretSchemas

class MaleoSecuritySecretGeneralTransfers:
    class Base(
        MaleoSecuritySecretSchemas.Data,
        MaleoSecuritySecretSchemas.Name
    ): pass