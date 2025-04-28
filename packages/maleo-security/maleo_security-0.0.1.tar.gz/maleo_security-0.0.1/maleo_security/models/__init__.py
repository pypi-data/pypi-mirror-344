from __future__ import annotations
from .schemas import MaleoSecuritySchemas
from .transfers import MaleoSecurityTransfers
from .responses import MaleoSecurityResponses

class MaleoSecurityModels:
    Schemas = MaleoSecuritySchemas
    Transfers = MaleoSecurityTransfers
    Responses = MaleoSecurityResponses