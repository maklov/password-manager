from pydantic.v1 import BaseModel


class EncryptedPasswordPayload(BaseModel):
    iv: str
    ciphertext: str
