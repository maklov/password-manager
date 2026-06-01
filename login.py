from pydantic import BaseModel


class LoginRequest(BaseModel):
    email: str = ""
    server_auth_hash: str = ""


class LoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class RegisterRequest(BaseModel):
    email: str
    server_auth_hash: str
    salt: str


class RegisterResponse(BaseModel):
    pass
