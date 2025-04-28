from __future__ import annotations
from pydantic import BaseModel, Field
from maleo_security.models.schemas.token import MaleoSecurityTokenSchemas

class MaleoSecurityTokenGeneralTransfers:
    class Payload(BaseModel):
        payload:MaleoSecurityTokenSchemas.Payload = Field(..., description="Payload")