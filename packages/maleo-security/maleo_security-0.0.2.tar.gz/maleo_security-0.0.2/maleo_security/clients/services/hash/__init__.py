from __future__ import annotations
from .bcrypt import MaleoSecurityBcryptHashClientService
from .hmac import MaleoSecurityHMACHashClientService
from .sha256 import MaleoSecuritySHA256HashClientService

class MaleoSecurityHashClientService:
    Bcrypt = MaleoSecurityBcryptHashClientService
    HMAC = MaleoSecurityHMACHashClientService
    SHA256 = MaleoSecuritySHA256HashClientService