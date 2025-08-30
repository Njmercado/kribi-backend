from fastapi import APIRouter, Depends
from app.service import words
from app.db import SessionDep

router = APIRouter(
  prefix="/word",
)

@router.get("/{word}")
def get_word(session: SessionDep, word: str):
	return words.get_word(session, word)

@router.get("/{letter}")
def get_all_words_from_letter(letter: str):
	return words.get_all_words_from_letter(letter)

# @router.delete("/{word}", dependencies=[Depends(False)])
@router.delete("/{word}")
def delete_word(word: str):
	return words.delete_word(word)

# @router.post("/", dependencies=[Depends(False)])
@router.post("/")
def create_word(word: str):
	return words.create_word(word)
