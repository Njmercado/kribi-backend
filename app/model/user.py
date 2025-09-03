from sqlmodel import SQLModel, Field, Column, ARRAY, String
from datetime import datetime
from enum import Enum
from typing import Optional

class Role(Enum):
  WORD_ADMIN = 'WORD_ADMIN'
  ARTICLE_ADMIN = 'ARTICLE_ADMIN'
  SUPER_ADMIN = 'SUPER_ADMIN'
  EDITOR = 'EDITOR'
  VIEWER = 'VIEWER'

class Entitlement(Enum):
  EDIT_WORD = 'EDIT_WORD'
  CREATE_WORD = 'CREATE_WORD'
  DELETE_WORD = 'DELETE_WORD'
  VIEW_WORD = 'VIEW_WORD'
  EDIT_ARTICLE = 'EDIT_ARTICLE'
  CREATE_ARTICLE = 'CREATE_ARTICLE'
  DELETE_ARTICLE = 'DELETE_ARTICLE'
  VIEW_ARTICLE = 'VIEW_ARTICLE'
  CREATE_USER = 'CREATE_USER'
  DELETE_USER = 'DELETE_USER'
  VIEW_USER = 'VIEW_USER'
  UPDATE_USER = 'UPDATE_USER'
  RESTORE_USER = 'RESTORE_USER'
  NONE = 'NONE'

class User(SQLModel, table=True):

  __allow_unmapped__ = True

  id: int = Field(primary_key=True, nullable=False, unique=True, index=True)
  email: str = Field(nullable=False, unique=True, index=True)
  name: str = Field(nullable=False)
  last_name: str = Field(nullable=False)
  full_name: str = Field(max_length=100, nullable=False)
  hashed_password: str = Field(nullable=False)
  username: str = Field(nullable=False, max_length=100, unique=True, index=True)
  is_active: bool = Field(default=True)
  is_superuser: bool = Field(default=False)
  role: Role = Field(default=Role.VIEWER)
  phone: Optional[str] = Field(default=None)
  location: Optional[str] = Field(default=None)
  entitlements: list[str] = Field(default=[Entitlement.NONE.value], sa_column=Column(ARRAY(String)))
  created_at: datetime = Field(default_factory=datetime.now)
  updated_at: datetime = Field(default_factory=datetime.now)

# Pydantic models for request/response
class UserCreate(SQLModel):
  email: str
  username: str
  name: str
  last_name: str
  password: str

class UserLogin(SQLModel):
  email: str
  password: str

class UserResponse(SQLModel):
  id: int
  email: str
  username: str
  name: str
  last_name: str
  full_name: str
  is_active: bool
  role: Role
  created_at: datetime
