from model.user import User
from db import SessionDep
from sqlmodel import select
from typing import Optional

def get_user_by_id(session: SessionDep, user_id: int) -> Optional[User]:
  """Get user by ID."""
  return session.exec(
    select(User)
    .where(User.id == user_id, User.is_active == True)
  ).first()

def get_user_by_email(session: SessionDep, email: str) -> Optional[User]:
  """Get user by email."""
  return session.exec(
    select(User)
    .where(User.email == email, User.is_active == True)
  ).first()

def get_user_by_username(session: SessionDep, username: str) -> Optional[User]:
  """Get user by username."""
  return session.exec(
    select(User)
    .where(User.username == username, User.is_active == True)
  ).first()

def create_user(session: SessionDep, user: User) -> User:
  """Create a new user."""
  session.add(user)
  session.commit()
  session.refresh(user)
  return user

def update_user(session: SessionDep, user: User) -> User:
  """Update an existing user."""
  session.add(user)
  session.commit()
  session.refresh(user)
  return user
