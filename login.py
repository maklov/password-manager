from dataclasses import dataclass

from pydantic.v1 import BaseModel


class LoginRequest(BaseModel):
    email = ""
    auth_hash = ""

class LoginResponse(BaseModel):
    access_token:str
    token_type: str = "bearer"