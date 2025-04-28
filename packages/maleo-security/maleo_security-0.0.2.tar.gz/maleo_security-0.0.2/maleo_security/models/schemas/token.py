from __future__ import annotations
from datetime import datetime, timedelta, timezone
from pydantic import BaseModel, Field, model_validator
from uuid import UUID
from maleo_foundation.types import BaseTypes
from maleo_security.enums.token import MaleoSecurityTokenEnums
from maleo_security.constants.token import REFRESH_TOKEN_DURATION_DAYS, ACCESS_TOKEN_DURATION_MINUTES

class MaleoSecurityTokenSchemas:
    class Key(BaseModel):
        key:str = Field(..., description="Key")

    class Token(BaseModel):
        token:str = Field(..., description="Token")

    class Payload(BaseModel):
        t:MaleoSecurityTokenEnums.TokenType = Field(..., description="Token Type")
        sr:UUID = Field(..., description="System role")
        u:UUID = Field(..., description="user")
        o:BaseTypes.OptionalUUID = Field(..., description="Organization")
        uor:BaseTypes.OptionalListOfUUIDs = Field(..., description="User Organization Role")
        iat_dt:datetime = Field(datetime.now(timezone.utc), description="Issued at (datetime)")
        iat:int = Field(..., description="Issued at (integer)")
        exp_dt:datetime = Field(..., description="Expired at (datetime)")
        exp:int = Field(..., description="Expired at (integet)")

        @model_validator(mode="before")
        @classmethod
        def set_iat_and_exp(cls, values:dict):
            iat_dt = values.get("iat_dt", None)
            if not iat_dt:
                iat_dt = datetime.now(timezone.utc)
            else:
                if not isinstance(iat_dt, datetime):
                    iat_dt = datetime.fromisoformat(iat_dt)
            values["iat_dt"] = iat_dt
            #* Convert `iat` to timestamp (int)
            values["iat"] = int(iat_dt.timestamp())
            exp_dt = values.get("exp_dt", None)
            if not exp_dt:
                if values["t"] == MaleoSecurityTokenEnums.TokenType.REFRESH:
                    exp_dt = iat_dt + timedelta(days=REFRESH_TOKEN_DURATION_DAYS)
                elif values["t"] == MaleoSecurityTokenEnums.TokenType.ACCESS:
                    exp_dt = iat_dt + timedelta(minutes=ACCESS_TOKEN_DURATION_MINUTES)
            else:
                if not isinstance(exp_dt, datetime):
                    exp_dt = datetime.fromisoformat(exp_dt)
            values["exp_dt"] = exp_dt
            #* Convert `exp_dt` to timestamp (int)
            values["exp"] = int(exp_dt.timestamp())
            return values