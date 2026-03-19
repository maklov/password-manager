from enum import unique

from dotenv import load_dotenv
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import sessionmaker, declarative_base, relationship
import os

load_dotenv()
db_link = os.getenv("DB_LINK")

engine = create_engine(db_link)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    server_auth_hash = Column(String, nullable=False)
    salt = Column(String, nullable=False)

    entries = relationship("Entry", back_populates="owner")

class Entry(Base):
    __tablename__ = "entries"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    ciphertext = Column(String, nullable=False)
    iv = Column(String, nullable=False)

    owner = relationship("User", back_populates="entries")

Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()