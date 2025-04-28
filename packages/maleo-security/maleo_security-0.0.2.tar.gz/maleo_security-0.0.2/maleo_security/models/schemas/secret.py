from pydantic import BaseModel, Field

class MaleoSecuritySecretSchemas:
    class Name(BaseModel):
        name:str = Field(..., description="Name")

    class Data(BaseModel):
        data:str = Field(..., description="Data")

    class Version(BaseModel):
        version:str = Field("latest", description="Version")