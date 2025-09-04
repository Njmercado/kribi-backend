from db import SessionDep
from data import articles
from fastapi import HTTPException
from model.article import Article, ArticleDTO, CreateArticle
from model.user import User
from fastapi import exceptions
from utils.responses import ARTICLE_CREATED_SUCCESSFULLY, ARTICLE_DELETED_SUCCESSFULLY, ARTICLE_UPDATED_SUCCESSFULLY
from fastapi import Response

def get_article_by_id(session: SessionDep, article_id: int) -> ArticleDTO:
  try:
    return articles.get_article_by_id(session, article_id)
  except exceptions.ValidationException as e:
    raise HTTPException(status_code=404, detail=str(e))
  except Exception as e:
    raise HTTPException(status_code=500, detail=str(e))

def get_articles_by_name(session: SessionDep, name: str) -> list[ArticleDTO]:
  try:
    return articles.get_articles_by_name(session, name)
  except exceptions.ValidationException as e:
    raise HTTPException(status_code=404, detail=str(e))
  except Exception as e:
    raise HTTPException(status_code=500, detail=str(e))

def create_article(session: SessionDep, user: User, article: CreateArticle):
  try:
    return articles.create_article(session, user, article)
  except exceptions.ValidationException as e:
    raise HTTPException(status_code=404, detail=str(e))
  except Exception as e:
    raise HTTPException(status_code=500, detail=str(e))

def update_article(session: SessionDep, current_user: User, article_id: int, article_data: Article) -> Response:
  try:
    return articles.update_article(session, current_user, article_id, article_data)
  except exceptions.ValidationException as e:
    raise HTTPException(status_code=404, detail=str(e))
  except Exception as e:
    raise HTTPException(status_code=500, detail=str(e))

def delete_article(session: SessionDep, current_user: User, article_id: int) -> Response:
  try:
    articles.delete_article(session, current_user, article_id)
    return ARTICLE_DELETED_SUCCESSFULLY(article_id)
  except exceptions.ValidationException as e:
    raise HTTPException(status_code=404, detail=str(e))
  except Exception as e:
    raise HTTPException(status_code=500, detail=str(e))
