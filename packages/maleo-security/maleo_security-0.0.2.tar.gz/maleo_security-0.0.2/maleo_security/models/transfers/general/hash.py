from __future__ import annotations
from maleo_security.models.schemas.hash import MaleoSecurityHashSchemas

class MaleoSecurityHashGeneralTransfers:
    class Hash(MaleoSecurityHashSchemas.Hash): pass
    class Verify(MaleoSecurityHashSchemas.IsValid): pass