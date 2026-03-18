from fastapi import FastAPI
from data_model import EncryptedPasswordPayload


server = FastAPI()

@server.get("/{token}/entries")
async def get_all_entries():
    pass

@server.get("/{token}/entries/{item}")
async def get_entry():
    pass

@server.post("/{token}/entries")
async def add_entry():
    pass

@server.put("/{token}/entries/{entry_id}/{item}")
async def edit_entry(item: EncryptedPasswordPayload):
    return {"message": "Saved successfully", "received_item":item.iv}
