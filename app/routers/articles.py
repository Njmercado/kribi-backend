from fastapi import APIRouter
from dependencies.auth import ViewArticleRequired
from db import SessionDep
from service import articles
from dependencies.auth import get_current_active_user
from fastapi import Depends
from model.user import User

router = APIRouter(
  prefix="/articles",
  tags=["articles"],
  responses={404: {"description": "Not found"}},
)

@router.get("/{article_id}", dependencies=[ViewArticleRequired])
def get_article(session: SessionDep, article_id: int):
  return articles.get_article_by_id(session, article_id)

@router.post("/", dependencies=[ViewArticleRequired])
def create_article(session: SessionDep, article_data: articles.Article, current_user: User = Depends(get_current_active_user)):
  return articles.create_article(session, current_user, article_data)
