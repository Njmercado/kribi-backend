from db import SessionDep
from data import articles
from fastapi import HTTPException
from model.article import Article
from model.user import User

def get_article_by_id(session: SessionDep, article_id: int):
  try:
    return articles.get_article_by_id(session, article_id)
  except Exception as e:
    raise HTTPException(status_code=500, detail=str(e))

def create_article(session: SessionDep, user: User, article_data: Article):
  try:
    return articles.create_article(session, user, article_data)
  except Exception as e:
    raise HTTPException(status_code=500, detail=str(e))
