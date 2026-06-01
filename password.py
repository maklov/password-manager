from typing import Optional
from pydantic import BaseModel


class EncryptedPasswordPayload(BaseModel):
    iv: str
    ciphertext: str
    notes_ciphertext: Optional[str] = None
    notes_iv: Optional[str] = None