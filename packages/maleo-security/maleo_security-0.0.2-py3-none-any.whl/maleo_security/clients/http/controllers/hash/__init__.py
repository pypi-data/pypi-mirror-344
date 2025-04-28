from __future__ import annotations
from .bcrypt import MaleoSecurityBcryptHashHTTPClientController
from .hmac import MaleoSecurityHMACHashHTTPClientController
from .sha256 import MaleoSecuritySHA256HashHTTPClientController

class MaleoSecurityHashHTTPClientController:
    Bcrypt = MaleoSecurityBcryptHashHTTPClientController
    HMAC = MaleoSecurityHMACHashHTTPClientController
    SHA256 = MaleoSecuritySHA256HashHTTPClientController