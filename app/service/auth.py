import os
from datetime import datetime, timedelta, timezone
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import HTTPException, status
from db import SessionDep
from data import users
from model.user import User
from model.auth import TokenData, Token

# Configuration
SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-here-change-this-in-production")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password: str, hashed_password: str) -> bool:
  """Verify a plain password against its hash."""
  return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
  """Hash a password."""
  return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
  """Create a JWT access token."""
  to_encode = data.copy()
  if expires_delta:
    expire = datetime.now(timezone.utc) + expires_delta
  else:
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
  to_encode.update({"exp": expire})
  encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
  return encoded_jwt

def verify_token(token: str) -> TokenData:
  """Verify and decode a JWT token."""
  credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
  )

  try:
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    email: str = payload.get("sub")
    if email is None:
      raise credentials_exception
    token_data = TokenData(email=email)
  except JWTError:
    raise credentials_exception
  except Exception:
    raise credentials_exception

  return token_data

def authenticate_user(session: SessionDep, email: str, password: str) -> Optional[User]:
  """Authenticate a user by email and password."""
  user = users.get_user_by_email(session, email)
  if not user:
    return None
  if not verify_password(password, user.hashed_password):
    return None
  return user

def login(session: SessionDep, email: str, password: str) -> Token:
  """Login user and return JWT token."""

  user = authenticate_user(session, email, password)
  if not user:
    raise HTTPException(
      status_code=status.HTTP_401_UNAUTHORIZED,
      detail="Incorrect email or password",
      headers={"WWW-Authenticate": "Bearer"},
    )

  if not user.is_active:
    raise HTTPException(
      status_code=status.HTTP_400_BAD_REQUEST,
      detail="Inactive user"
    )

  access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
  access_token = create_access_token(
    data={"sub": user.email}, 
    expires_delta=access_token_expires
  )

  return Token(access_token=access_token, token_type="bearer")
