from typing import List

from fastapi import APIRouter, Depends, Form, HTTPException
from fastapi.routing import APIRouter
from sqlalchemy.orm import Session

from . import crud, schemas
from .db import SessionLocal

router = APIRouter()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# User routes
@router.post("/users/", response_model=schemas.User, tags=["user"])
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    """
    Create user
    """
    db_user_by_email = crud.get_user_by_email(
        db=db,
        email=user.email
    )
    db_user_by_username = crud.get_user_by_username(
        db=db,
        username=user.username
    )

    if db_user_by_email:
        raise HTTPException(
            status_code=400,
            detail="Email already registered."
        )
    if db_user_by_username:
        raise HTTPException(
            status_code=400,
            detail="Usesrname already registered."
        )

    return crud.create_user(db=db, user=user)


@router.get("/users/u{user_id}", response_model=schemas.User, tags=["user"])
def get_user_by_id(user_id: int, db: Session = Depends(get_db)):
    """
    Get user by given ID
    """
    db_user = crud.get_user_by_id(db=db, user_id=user_id)

    if not db_user:
        raise HTTPException(status_code=404, detail="User not found.")

    return db_user


@router.get("/users/{username}", response_model=schemas.User, tags=["user"])
def get_user_by_username(username: str, db: Session = Depends(get_db)):
    """
    Get user by given username
    """
    db_user = crud.get_user_by_username(db=db, username=username)

    if not db_user:
        raise HTTPException(status_code=404, detail="User not found.")

    return db_user


@router.get("/users/", response_model=List[schemas.User], tags=["user"])
def get_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Get all users
    """
    db_users = crud.get_users(db=db, skip=skip, limit=limit)

    return db_users


@router.put("/users/{user_id}/update/", response_model=schemas.User, tags=["user"])
def update_user(user_id: int,
                db: Session = Depends(get_db),
                username: str = Form(default=None),
                first_name: str = Form(default=None),
                last_name: str = Form(default=None)):
    """
    Update user by ID
    """
    to_change = {
        "username": username,
        "first_name": first_name,
        "last_name": last_name,
    }
    updated_user = crud.update_user(
        db=db,
        user_id=user_id,
        to_change=to_change,
    )

    if not updated_user:
        raise HTTPException(status_code=404, detail="Some Error has Occured.")

    return crud.get_user_by_id(db=db, user_id=user_id)


@router.delete("/users/{user_id}/delete/", tags=["user"])
def delete_user(user_id: int, db: Session = Depends(get_db)):
    """
    Delete user by ID
    """
    deleted_user = crud.delete_user(db=db, user_id=user_id)

    return {"status": "ok"} if deleted_user else {"status": "fail"}


# Note routes
@router.post("/notes/", response_model=schemas.Note, tags=["notes"])
def create_note(note: schemas.NoteCreate, user_id: int, db: Session = Depends(get_db)):
    """
    Create note by Note model and user_id
    """
    return crud.create_note(db=db, note=note, user_id=user_id)


@router.get("/users/{user_id}/notes/{note_id}", response_model=schemas.Note, tags=["notes"])
def get_note(user_id: int, note_id: int, db: Session = Depends(get_db)):
    """
    Get note by ID and user_id
    """
    db_user = crud.get_user_by_id(db=db, user_id=user_id)

    if note_id not in (note.id for note in db_user.notes):
        raise HTTPException(status_code=404, detail="Note not found.")

    return crud.get_note(db=db, note_id=note_id, user_id=user_id)


@router.get("/users/{user_id}/notes/", response_model=List[schemas.Note], tags=["notes"])
def get_notes_by_user(user_id: int, db: Session = Depends(get_db)):
    """
    Get all notes by user
    """
    return crud.get_all_notes_by_user(db=db, user_id=user_id)


@router.get("/notes/", response_model=List[schemas.Note], tags=["notes"])
def get_notes(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Get all notes
    """
    return crud.get_notes(db=db, skip=skip, limit=limit)


@router.put("/users/{user_id}/notes/{note_id}/update/", response_model=schemas.Note, tags=["notes"])
def update_note(user_id: int,
                note_id: int,
                db: Session = Depends(get_db),
                title: str = Form(default=None),
                body: str = Form(default=None)):
    """
    Update note by ID and user_id
    """
    db_user = crud.get_user_by_id(db=db, user_id=user_id)
    if note_id not in (note.id for note in db_user.notes):
        raise HTTPException(status_code=404, detail="Note not found.")

    to_change = {"title": title, "body": body}
    crud.update_note(
        db=db, user_id=user_id,
        note_id=note_id, to_change=to_change
    )

    return crud.get_note(db=db, note_id=note_id, user_id=user_id)


@router.delete("/users/{user_id}/notes/{note_id}/delete/", tags=["notes"])
def delete_note(user_id: int, note_id: int, db: Session = Depends(get_db)):
    """
    Delete note by ID and user_id
    """
    deleted_note = crud.delete_note(db=db, note_id=note_id, user_id=user_id)

    return {"detail": "ok"} if deleted_note else {"detail": "fail"}
