from model.user import User, UserCreateDTO, UserUpdateDTO
from db import SessionDep
from sqlmodel import select, or_, func
from typing import Optional
from utils.auth import get_password_hash

def get_user_by_id(session: SessionDep, user_id: int) -> Optional[User]:
  """Get user by ID."""
  return session.exec(
    select(User)
    .where(User.id == user_id)
  ).first()

def search_user(session: SessionDep, current_user_id: int, regex_subs: str, page: int, limit: int):
  filters = or_(
    func.lower(User.username).op("~")(regex_subs),
    func.lower(User.email).op("~")(regex_subs),
    func.lower(User.name).op("~")(regex_subs),
    func.lower(User.name).op("~")(regex_subs)
  )

  result = session.exec(
    select(User)
    .where(
      filters,
      User.id != current_user_id,
    )
    .offset((page - 1) * limit)
    .limit(limit + 1)  # Fetch one extra to check if there's a next
  ).all()

  has_next_page = len(result) > limit
  users = result[:limit]  # Return only the requested number of results

  return {
    "users": users,
    "has_next_page": has_next_page
  }


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

def create_user(session: SessionDep, user: UserCreateDTO, current_user_id: int) -> User:
  """Create a new user."""
  user_to_create = User()
  user_to_create.updated_at = user_to_create.created_at = func.now()
  user_to_create.email = user.email
  user_to_create.username = user.username
  user_to_create.name = user.name
  user_to_create.last_name = user.last_name
  user_to_create.full_name = f"{user.name} {user.last_name}"
  user_to_create.role = user.role
  user_to_create.entitlements = [entitlement.value for entitlement in user.entitlements]
  user_to_create.location = user.location
  user_to_create.phone = user.phone
  user_to_create.hashed_password = get_password_hash("Admin1234")
  session.add(user_to_create)
  session.commit()
  session.refresh(user_to_create)
  return user_to_create

def update_user(session: SessionDep, user_to_update: User, user_data: UserUpdateDTO) -> User:
  """Update an existing user."""
  for key, value in user_data.model_dump(exclude_unset=True).items():
    setattr(user_to_update, key, value)
  user_to_update.updated_at = func.now()
  user_to_update.entitlements = [entitlement.value for entitlement in user_data.entitlements]
  session.add(user_to_update)
  session.commit()
  session.refresh(user_to_update)
  return user_to_update

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