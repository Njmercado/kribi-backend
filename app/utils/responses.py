from fastapi import Response
import json

WORD_DELETED_SUCCESSFULLY = lambda: Response(status_code=204)
WORD_CREATED_SUCCESSFULLY = lambda x: Response(status_code=201, content=f"Word '{x}' created successfully :)")
ARTICLE_DELETED_SUCCESSFULLY = lambda x: Response(status_code=200, content=f"Article with id '{x}' deleted successfully :)")
ARTICLE_CREATED_SUCCESSFULLY = lambda x: Response(status_code=201, content={
  "data": x
})
ARTICLE_UPDATED_SUCCESSFULLY = lambda x: Response(status_code=200, content={
  "data": x
})
