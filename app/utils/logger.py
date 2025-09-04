import logging

LOGGER = logging.getLogger('uvicorn.error')

def log(input: str):
	LOGGER.debug(input)
