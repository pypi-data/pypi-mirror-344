from __future__ import annotations
from .bcrypt import MaleoSecurityBcryptHashParametersTransfers
from .hmac import MaleoSecurityHMACHashParametersTransfers
from .sha256 import MaleoSecuritySHA256HashParametersTransfers

class MaleoSecurityHashParametersTransfers:
    Bcrypt = MaleoSecurityBcryptHashParametersTransfers
    HMAC = MaleoSecurityHMACHashParametersTransfers
    SHA256 = MaleoSecuritySHA256HashParametersTransfers