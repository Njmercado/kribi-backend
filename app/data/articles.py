from db import SessionDep
from model.article import Article, ArticleDTO, ArticlesDTO, CreateArticle, CreatedArticle, UpdateArticle
from datetime import datetime
from model.user import User
from sqlmodel import select, update

def get_article_by_id(session: SessionDep, article_id: int) -> ArticleDTO:
  return session.exec(
    select(Article)
    .where(Article.id == article_id)
  ).first()

def get_articles_by_name(session: SessionDep, name: str, page: int, limit: int) -> ArticlesDTO:
  articles = session.exec(
    select(Article)
    .where(Article.title.ilike(f"%{name}%"), Article.deleted == False)
    .offset((page - 1) * limit)
    .limit(limit + 1)
  ).all()

  has_next_page = len(articles) > limit
  articles = articles[:limit]

  return {
    "articles": articles,
    "has_next_page": has_next_page
  }

def create_article(session: SessionDep, current_user: User, article: CreateArticle) -> CreatedArticle:
  article_to_create = Article.model_validate(article)
  article_to_create.created_at = article_to_create.updated_at = datetime.now()
  article_to_create.created_by = article_to_create.updated_by = current_user.id
  session.add(article_to_create)
  session.commit()
  session.refresh(article_to_create)
  return CreatedArticle.model_validate(article_to_create)

def update_article(session: SessionDep, current_user: User, article_id: int, article_data: UpdateArticle):
  # existing_article = get_article_by_id(session, article_id)
  existing_article = session.exec(
    select(Article)
    .where(Article.id == article_id, Article.deleted == False)
  ).first()

  if not existing_article:
    raise Exception(f"Article with id {article_id} not found or has been deleted")

  session.exec(
    update(Article)
    .where(Article.id == article_id)
    .values(
      title=article_data.title,
      content=article_data.content,
      summary=article_data.summary,
      cover=article_data.cover,
      public=article_data.public,
      tags=article_data.tags,
      authors=article_data.authors,
      updated_at=datetime.now(),
      updated_by=current_user.id
    )
  )
  session.commit()
  session.refresh(existing_article)

def delete_article(session: SessionDep, current_user: User, article_id: int):
  existing_article = get_article_by_id(session, article_id)
  existing_article.deleted = True
  existing_article.updated_at = datetime.now()
  existing_article.updated_by = current_user.id
  session.add(existing_article)
  session.commit()
