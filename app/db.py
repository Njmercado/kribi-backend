import os
from sqlmodel import create_engine, Session, SQLModel
from fastapi import Depends
from typing import Annotated

POSTGRES_USER = os.getenv("POSTGRES_USER", "postgres")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "example")
POSTGRES_HOST = os.getenv("POSTGRES_HOST", "localhost")
POSTGRES_PORT = os.getenv("POSTGRES_PORT", "5432")
POSTGRES_DB = os.getenv("POSTGRES_DB", "kribi")

DATABASE_URL = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"

# SQLModel setup
engine = create_engine(DATABASE_URL)

# Dependency to get database session
def get_session():
  with Session(engine) as session:
    yield session

def create_db_and_tables():
  SQLModel.metadata.create_all(engine)

SessionDep = Annotated[Session, Depends(get_session)]
