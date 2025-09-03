from fastapi import APIRouter, Depends, Path, Body
from service import words
from db import SessionDep
from typing import Annotated
from model.word import Word
from model.user import User
from dependencies.auth import (
  get_current_active_user, 
  CreateWordRequired, 
  EditWordRequired, 
  DeleteWordRequired,
  WordAdminRequired
)

router = APIRouter(
  prefix="/word",
  tags=["words"]
)

# Public endpoints (no authentication required)
@router.get("/id/{word_id}")
def get_word_by_id(session: SessionDep, word_id: int):
  """Get word by ID - Public access"""
  return words.get_word_by_id(session, word_id)

@router.get("/{word}")
def get_word(session: SessionDep, word: Annotated[str, Path(min_length=1)]):
  """Get word by name - Public access"""
  return words.get_word(session, word)

@router.get("/filter/{letter}")
def get_filtered_words_by_letter(session: SessionDep, letter: Annotated[str, Path(max_length=2)]):
  """Get words filtered by letter - Public access"""
  return words.get_all_words_from_letter(session, letter)

@router.get("/search/{substring}")
def search_words(session: SessionDep, substring: Annotated[str, Path(min_length=3)]):
  """Search words by substring - Public access"""
  return words.search_words(session, substring)

# Protected endpoints (authentication + specific permissions required)
@router.post("/", dependencies=[CreateWordRequired])
def create_word(
  session: SessionDep, 
  word: Annotated[Word, Body(embed=True)],
  current_user: User = Depends(get_current_active_user)
):
  """Create a new word - Requires CREATE_WORD entitlement or admin role"""
  return words.create_word(session, word)

@router.put("/{word_id}", dependencies=[EditWordRequired])
def update_word(
  session: SessionDep, 
  word_id: int, 
  word: Annotated[Word, Body(embed=True)],
  current_user: User = Depends(get_current_active_user)
):
  """Update an existing word - Requires EDIT_WORD entitlement or admin role"""
  return words.update_word(session, word_id, word)

@router.delete("/{word_id}", dependencies=[DeleteWordRequired])
def delete_word(
  session: SessionDep, 
  word_id: int,
  current_user: User = Depends(get_current_active_user)
):
  """Delete a word - Requires DELETE_WORD entitlement or admin role"""
  return words.delete_word(session, word_id)
