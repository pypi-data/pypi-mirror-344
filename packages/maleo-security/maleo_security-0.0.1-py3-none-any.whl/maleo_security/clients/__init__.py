from __future__ import annotations
from .http import MaleoSecurityHTTPClient
from .services import MaleoSecurityClientServices

class MaleoSecurityClients:
    HTTP = MaleoSecurityHTTPClient
    Services = MaleoSecurityClientServices