from sqlmodel import SQLModel, Field, Column, ARRAY, String, Integer
from datetime import datetime

class Article(SQLModel, table=True):
  id: int = Field(default=None, primary_key=True, index=True)
  title: str = Field(nullable=False)
  content: str = Field(nullable=False)
  summary: str = Field(default="", nullable=False)
  created_at: datetime = Field(default_factory=datetime.now)
  updated_at: datetime = Field(default_factory=datetime.now)
  deleted: bool = Field(default=False)
  authors: list[int] = Field(sa_column=Column(ARRAY(Integer), server_default='{}'))
  created_by: int = Field(default=None, foreign_key="user.id")
  updated_by: int = Field(default=None, foreign_key="user.id")
  public: bool = Field(default=True)
  tags: list[str] = Field(default=[], sa_column=Column(ARRAY(String), server_default='{}'))

class CreateArticle(SQLModel):
	title: str
	content: str
	summary: str = ""
	authors: list[int] = []
	public: bool = True
	tags: list[str] = []

class CreatedArticle(SQLModel):
  id: int
  title: str
  content: str
  summary: str
  authors: list[int]
  created_by: int
  public: bool
  tags: list[str]
  created_at: datetime

class ArticleDTO(SQLModel):
	id: int
	title: str
	content: str
	summary: str
	created_at: datetime
	updated_at: datetime
	authors: list[int]
	created_by: int
	updated_by: int
	public: bool
	tags: list[str]

class UpdateArticle(SQLModel):
	title: str
	content: str
	summary: str
	authors: list[int]
	public: bool = True
	tags: list[str]
	updated_at: datetime = datetime.now()
