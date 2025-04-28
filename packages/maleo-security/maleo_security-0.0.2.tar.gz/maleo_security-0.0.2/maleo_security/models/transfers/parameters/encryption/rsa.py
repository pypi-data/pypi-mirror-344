from maleo_security.models.schemas.encryption import MaleoSecurityEncryptionSchemas

class MaleoSecurityRSAEncryptionParametersTransfers:
    class EncryptSingle(
        MaleoSecurityEncryptionSchemas.Plaintext,
        MaleoSecurityEncryptionSchemas.Key
    ): pass

    class EncryptMultiple(
        MaleoSecurityEncryptionSchemas.ListOfPlaintext,
        MaleoSecurityEncryptionSchemas.Key
    ): pass

    class DecryptSingle(
        MaleoSecurityEncryptionSchemas.Ciphertext,
        MaleoSecurityEncryptionSchemas.Key
    ): pass

    class DecryptMultiple(
        MaleoSecurityEncryptionSchemas.ListOfCiphertext,
        MaleoSecurityEncryptionSchemas.Key
    ): pass