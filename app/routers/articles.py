from fastapi import APIRouter, Query
from dependencies.auth import ViewArticleRequired, EditArticleRequired, DeleteArticleRequired, CreateArticleRequired
from db import SessionDep
from service import articles
from dependencies.auth import get_current_active_user
from fastapi import Depends
from model.user import User
from model.article import Article, ArticlesDTO, CreateArticle, ArticleDTO, UpdateArticle
from typing import Annotated

router = APIRouter(
  prefix="/articles",
  tags=["articles"],
  responses={404: {"description": "Not found"}},
)

@router.get("/search", response_model=ArticlesDTO)
def get_articles_by_name(
  session: SessionDep,
  value: Annotated[str, Query(description="Search value")],
  page: Annotated[int, Query(ge=1, description="Page number")] = 1,
  limit: Annotated[int, Query(ge=1, le=100, description="Number of results per page")] = 10
):
  return articles.get_articles_by_name(session, value, page, limit)

@router.get("/{article_id}")
def get_article(session: SessionDep, article_id: int) -> ArticleDTO:
  return articles.get_article_by_id(session, article_id)

@router.post("/", dependencies=[CreateArticleRequired])
def create_article(session: SessionDep, article: CreateArticle, current_user: User = Depends(get_current_active_user)):
  return articles.create_article(session, current_user, article)

@router.put("/{article_id}", dependencies=[EditArticleRequired])
def update_article(session: SessionDep, article_id: int, article_data: UpdateArticle, current_user: User = Depends(get_current_active_user)):
  return articles.update_article(session, current_user, article_id, article_data)

@router.delete("/{article_id}", dependencies=[DeleteArticleRequired])
def delete_article(session: SessionDep, article_id: int, current_user: User = Depends(get_current_active_user)):
  return articles.delete_article(session, current_user, article_id)
