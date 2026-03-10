from model.user import User, UserUpdateDTO
from db import SessionDep
from sqlmodel import select
from typing import Optional

def get_user_by_name(session: SessionDep, name: str) -> Optional[User]:
  """Get user by name."""
  return session.exec(
    select(User)
    .where(User.name == name, User.is_active == True)
  ).first()

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

def update_user(session: SessionDep, current_user: User, user: UserUpdateDTO) -> User:
  """Update an existing user."""
  user.updated_by = current_user.id
  session.add(user)
  session.commit()
  session.refresh(user)
  return user

def restore_user(session: SessionDep, user: User) -> User:
  """Restore a deleted user."""
  user.is_active = True
  session.add(user)
  session.commit()
  session.refresh(user)
  return user

def delete_user(session: SessionDep, user: User):
  """Soft delete a user."""
  user.is_active = False
  session.add(user)
  session.commit()
  session.refresh(user)