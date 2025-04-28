from maleo_security.models.schemas.encryption import MaleoSecurityEncryptionSchemas

class MaleoSecurityRSAEncryptionGeneralTransfers:
    class SingleEncryption(MaleoSecurityEncryptionSchemas.Ciphertext): pass
    class MultipleEncryption(MaleoSecurityEncryptionSchemas.ListOfCiphertext): pass
    class SingleDecryption(MaleoSecurityEncryptionSchemas.Plaintext): pass
    class MultipleDecryption(MaleoSecurityEncryptionSchemas.ListOfPlaintext): pass