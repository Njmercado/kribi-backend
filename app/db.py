import os
from dotenv import load_dotenv
from sqlmodel import create_engine, Session, SQLModel
from fastapi import Depends
from typing import Annotated

load_dotenv()

POSTGRES_USER = os.getenv("POSTGRES_USER", "postgres")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "example")
POSTGRES_HOST = os.getenv("POSTGRES_HOST", "localhost")
POSTGRES_PORT = os.getenv("POSTGRES_PORT", "5432")
POSTGRES_DB = os.getenv("POSTGRES_DB", "kribi")

DATABASE_URL = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"

# SQLModel setup with optimized connection pool configuration
engine = create_engine(
  DATABASE_URL,
  pool_size=5,           # Base connections (sufficient for single API instance)
  max_overflow=10,       # Extra connections during high load (total max: 15)
  pool_timeout=20,       # Seconds to wait for connection (fail fast)
  pool_recycle=3600,     # Recreate connections every hour (prevents stale connections)
  pool_pre_ping=True     # Test connections before use (prevents connection errors)
)

# Dependency to get database session
def get_session():
  with Session(engine) as session:
    yield session

def create_db():
  try:
    SQLModel.metadata.create_all(engine)
    print("✅ Database tables created/verified successfully")
  except Exception as e:
    print(f"⚠️  Database table creation failed: {e}")
    # Don't raise - let app start even if tables exist

def close_db_connections():
  """Close all database connections and dispose of the engine."""
  engine.dispose()

def get_connection_info():
  """Get current connection pool information."""
  pool = engine.pool
  return {
    "pool_size": pool.size(),           # Total connections currently in the pool
    "checked_in": pool.checkedin(),     # Available/idle connections ready to use
    "checked_out": pool.checkedout(),   # Active connections currently being used
    "overflow": pool.overflow(),        # Extra connections beyond base pool_size
    "total_max": pool.size() + pool.overflow(),  # Maximum possible connections
    "utilization": f"{pool.checkedout()}/{pool.size() + pool.overflow()}"  # Usage ratio
  }

SessionDep = Annotated[Session, Depends(get_session)]
