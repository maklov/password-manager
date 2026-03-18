from pydantic.v1 import BaseModel
import json



class EncryptedPasswordPayload(BaseModel):
    def __init__(self):
        super().__init__()

        self.iv = ""  # wektor inicjalizacyjny
        self.cypher: json # zaszyfrowany ciag znakow