from sqlmodel import SQLModel, Field, Column, ARRAY, String, Integer
from datetime import datetime

class Article(SQLModel, table=True):
  id: int = Field(default=None, primary_key=True, index=True)
  title: str = Field()
  content: str = Field()
  summary: str = Field(default="")
  created_at: datetime = Field(default_factory=datetime.now)
  updated_at: datetime = Field(default_factory=datetime.now)
  deleted: bool = Field(default=False)
  authors: list[int] = Field(sa_column=Column(ARRAY(Integer), server_default='{}'))
  created_by: int = Field(default=None, foreign_key="user.id")
  updated_by: int = Field(default=None, foreign_key="user.id")
  public: bool = Field(default=True)
  tags: list[str] = Field(default=[], sa_column=Column(ARRAY(String), server_default='{}'))
