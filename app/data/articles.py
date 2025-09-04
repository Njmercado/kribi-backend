from db import SessionDep
from model.article import Article
from datetime import datetime
from model.user import User

def get_article_by_id(session: SessionDep, article_id: int):
  return session.select(Article).where(Article.id == article_id).first()

def create_article(session: SessionDep, current_user: User, article_data: Article):
  article_data.created_at = article_data.updated_at = datetime.now()
  article_data.created_by = article_data.updated_by = current_user.id
  session.add(article_data)
  session.commit()
  session.refresh(article_data)
  return article_data
