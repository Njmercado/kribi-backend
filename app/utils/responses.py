from fastapi import Response
import json

WORD_DELETED_SUCCESSFULLY = lambda: Response(status_code=204)
WORD_CREATED_SUCCESSFULLY = lambda x: Response(status_code=201)
ARTICLE_DELETED_SUCCESSFULLY = lambda x: Response(status_code=200)
ARTICLE_CREATED_SUCCESSFULLY = lambda x: Response(status_code=201, content={
  "data": x
})
ARTICLE_UPDATED_SUCCESSFULLY = lambda x: Response(status_code=200, content={
  "data": x
})

USER_RESTORED_SUCCESSFULLY = lambda x: Response(status_code=200, content={
  "message": f"User with ID {x} restored successfully."
})
USER_DELETED_SUCCESSFULLY = lambda x: Response(status_code=200, content={
  "message": f"User with ID {x} deleted successfully."
})