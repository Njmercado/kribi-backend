from fastapi import APIRouter

router = APIRouter(
  prefix="/articles",
)

@router.get("/{article_id}")
def get_article(article_id: int):
	return {"article_id": article_id}