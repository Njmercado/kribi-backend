from db import SessionDep
from model.article import Article, ArticleDTO, CreateArticle, CreatedArticle
from datetime import datetime
from model.user import User

def get_article_by_id(session: SessionDep, article_id: int) -> ArticleDTO:
  return ArticleDTO.model_validate(
    session
      .select(Article)
      .where(Article.id == article_id)
      .first()
  )

def get_articles_by_name(session: SessionDep, name: str) -> list[ArticleDTO]:
  articles = session \
    .select(Article) \
    .where(Article.title.ilike(f"%{name}%")) \
    .all()
  return [ArticleDTO.model_validate(article) for article in articles]

def create_article(session: SessionDep, current_user: User, article: CreateArticle) -> CreatedArticle:
  article_to_create = Article.model_validate(article)
  article_to_create.created_at = article_to_create.updated_at = datetime.now()
  article_to_create.created_by = article_to_create.updated_by = current_user.id
  session.add(article_to_create)
  session.commit()
  session.refresh(article_to_create)
  return CreatedArticle.model_validate(article_to_create)

def update_article(session: SessionDep, current_user: User, article_id: int, article_data: Article):
  existing_article = get_article_by_id(session, article_id)
  for key, value in article_data.model_dump(exclude_unset=True).items():
    setattr(existing_article, key, value)
  existing_article.updated_at = datetime.now()
  existing_article.updated_by = current_user.id
  session.add(existing_article)
  session.commit()
  session.refresh(existing_article)
  return existing_article

def delete_article(session: SessionDep, current_user: User, article_id: int):
  existing_article = get_article_by_id(session, article_id)
  existing_article.deleted = True
  existing_article.updated_at = datetime.now()
  existing_article.updated_by = current_user.id
  session.add(existing_article)
  session.commit()
  return existing_article
