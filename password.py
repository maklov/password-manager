from pydantic.v1 import BaseModel


class EncryptedPasswordPayload(BaseModel):
    def __init__(self):
        super().__init__()

        self.iv = ""
        self.ciphertext=""