from pydantic import BaseModel


class EncryptedPasswordPayload(BaseModel):
    iv: str
    ciphertext: str
