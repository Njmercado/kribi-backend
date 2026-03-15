from pydantic import BaseModel
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
  cover: str = Field(default="", nullable=True)

class CreateArticle(SQLModel):
	title: str
	content: str
	summary: str = ""
	authors: list[int] = []
	public: bool = True
	tags: list[str] = []
	cover: str = ""

class CreatedArticle(SQLModel):
  id: int
  title: str
  content: str
  summary: str
  authors: list[int]
  created_by: int
  public: bool
  tags: list[str]
  cover: str
  created_at: datetime

class ArticleDTO(BaseModel):
	id: int
	title: str
	content: str
	summary: str
	created_at: datetime
	updated_at: datetime
	authors: list[int]
	created_by: int
	public: bool
	tags: list[str]
	cover: str

class ArticlesDTO(BaseModel):
	articles: list[ArticleDTO]
	has_next_page: bool

class UpdateArticle(SQLModel):
	title: str
	content: str
	summary: str
	authors: list[int]
	public: bool = True
	tags: list[str]
	updated_at: datetime = datetime.now()
	cover: str

class ArticleSynopsisDTO(BaseModel):
	id: int
	title: str
	summary: str
	cover: str
	created_at: datetime