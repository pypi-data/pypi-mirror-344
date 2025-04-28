from maleo_security.models.schemas.secret import MaleoSecuritySecretSchemas

class MaleoSecuritySecretParametersTransfers:
    class Get(
        MaleoSecuritySecretSchemas.Version,
        MaleoSecuritySecretSchemas.Name
    ): pass

    class Create(
        MaleoSecuritySecretSchemas.Data,
        MaleoSecuritySecretSchemas.Name
    ): pass