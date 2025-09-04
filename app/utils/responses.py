from fastapi import Response

WORD_DELETED_SUCCESSFULLY = lambda x: Response(status_code=200, content=f"Word with id '{x}' deleted successfully :)")
WORD_CREATED_SUCCESSFULLY = lambda x: Response(status_code=201, content=f"Word '{x}' created successfully :)")
