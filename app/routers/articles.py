from fastapi import APIRouter
from dependencies.auth import ViewArticleRequired, EditArticleRequired, DeleteArticleRequired, CreateArticleRequired
from db import SessionDep
from service import articles
from dependencies.auth import get_current_active_user
from fastapi import Depends
from model.user import User
from model.article import Article, CreateArticle, ArticleDTO, UpdateArticle

router = APIRouter(
  prefix="/articles",
  tags=["articles"],
  responses={404: {"description": "Not found"}},
)

@router.get("/{article_id}")
def get_article(session: SessionDep, article_id: int) -> ArticleDTO:
  return articles.get_article_by_id(session, article_id)

@router.get("/search/{name}")
def get_articles_by_name(session: SessionDep, name: str) -> list[ArticleDTO]:
  return articles.get_articles_by_name(session, name)

@router.post("/", dependencies=[CreateArticleRequired])
def create_article(session: SessionDep, article: CreateArticle, current_user: User = Depends(get_current_active_user)):
  return articles.create_article(session, current_user, article)

@router.put("/{article_id}", dependencies=[EditArticleRequired])
def update_article(session: SessionDep, article_id: int, article_data: UpdateArticle, current_user: User = Depends(get_current_active_user)):
  return articles.update_article(session, current_user, article_id, article_data)

@router.delete("/{article_id}", dependencies=[DeleteArticleRequired])
def delete_article(session: SessionDep, article_id: int, current_user: User = Depends(get_current_active_user)):
  return articles.delete_article(session, current_user, article_id)
