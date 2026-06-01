import os

import jwt
from dotenv import load_dotenv
from fastapi import Depends, FastAPI, HTTPException
from starlette import status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from database import Entry, User, get_db
from login import LoginRequest, LoginResponse, RegisterRequest
from password import EncryptedPasswordPayload

load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")

server = FastAPI(title="Zero-Knowledge Password Manager API")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/login")


async def get_current_user(
    token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Couldn't verify token",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        # getting users id from token
        payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
        user_id_str: str = payload.get("sub")
        if user_id_str is None:
            raise credentials_exception
    except jwt.PyJWTError:
        raise credentials_exception

    # checking if user id is in DB
    user = db.query(User).filter(User.id == int(user_id_str)).first()
    if user is None:
        raise credentials_exception
    return user


@server.post("/api/login")
async def login(login_payload: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == login_payload.email).first()
    if not user or user.server_auth_hash != login_payload.server_auth_hash:
        raise HTTPException(status_code=401, detail="Incorrect email address or hash")
    token = jwt.encode({"sub": str(user.id)}, SECRET_KEY, algorithm=ALGORITHM)
    return LoginResponse(access_token=token)


@server.post("/api/register")
async def register(payload: RegisterRequest, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.email == payload.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email already exists",
        )
    new_user = User(
        email=payload.email,
        server_auth_hash=payload.server_auth_hash,
        salt=payload.salt,
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"status": "success", "message": "Account created successfully!"}


@server.get("/api/{email}/salt")
async def get_user_salt(email: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="No salt for given user"
        )

    return {"email": user.email, "salt": user.salt}


@server.get("/api/entries")
async def get_all_entries(
    current_user: User = Depends(get_current_user), db: Session = Depends(get_db)
):
    entries = db.query(Entry).filter(Entry.user_id == current_user.id).all()
    return entries


@server.post("/api/entries")
async def add_entry(
    item: EncryptedPasswordPayload,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    try:
        new_entry = Entry(
            user_id=current_user.id, ciphertext=item.ciphertext, iv=item.iv
        )
        db.add(new_entry)
        db.commit()
        db.refresh(new_entry)

        return {"status": "success", "id": new_entry.id}
    except Exception:
        raise HTTPException(status_code=500, detail="Couldn't add new entry")


@server.put("/api/entries/{entry_id}/")
async def edit_entry(
    entry_id: int,
    item: EncryptedPasswordPayload,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    entry = (
        db.query(Entry)
        .filter(Entry.user_id == current_user.id, Entry.id == entry_id)
        .first()
    )

    if not entry:
        raise HTTPException(status_code=404, detail="Entry not found.")

    entry.ciphertext = item.ciphertext
    entry.iv = item.iv

    db.commit()

    return {"status": "success", "message": "Entity updated!"}


@server.delete("/api/entries/{entry_id}")
async def delete_entry(
    entry_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    entry = (
        db.query(Entry)
        .filter(Entry.user_id == current_user.id, Entry.id == entry_id)
        .first()
    )

    if not entry:
        raise HTTPException(status_code=404, detail="Entry not found.")

    db.delete(entry)
    db.commit()

    return {"status": "success", "message": "Entity successfully deleted!"}
