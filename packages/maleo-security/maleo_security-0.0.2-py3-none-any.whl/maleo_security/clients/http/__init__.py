from __future__ import annotations
from .manager import MaleoSecurityHTTPClientManager
from .controllers import MaleoSecurityHTTPClientControllers

class MaleoSecurityHTTPClient:
    Manager = MaleoSecurityHTTPClientManager
    Controllers = MaleoSecurityHTTPClientControllers