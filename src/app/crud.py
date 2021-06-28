from typing import Dict

from sqlalchemy.orm import Session

from . import models, schemas


# User CRUD
def get_user_by_id(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.UserCreate):
    fake_password = f'some_strong_{user.password}'
    db_user = models.User(
        username=user.username,
        email=user.email,
        password=fake_password,
        first_name=user.first_name,
        last_name=user.last_name,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def update_user(db: Session, user_id: int, to_change: Dict[str, str]):
    to_change = {key: value for key, value in to_change.items() if value}

    if to_change:
        updated_user = db.query(models.User).\
            filter(models.User.id == user_id).\
            update(to_change, synchronize_session="fetch")

        db.commit()

    return updated_user


def delete_user(db: Session, user_id: int):
    deleted_user = db.query(models.User).\
        filter(models.User.id == user_id).\
        delete(synchronize_session="fetch")

    db.commit()
    return deleted_user


# Note CRUD
def get_note(db: Session, note_id: int, user_id: int):
    return db.query(models.Note).\
        filter(models.Note.id == note_id,
               models.Note.owner_id == user_id).\
        first()


def get_all_notes_by_user(db: Session, user_id: int):
    return db.query(models.Note).filter(models.Note.owner_id == user_id).all()


def get_notes(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Note).offset(skip).limit(limit).all()


def create_note(db: Session, note: schemas.NoteCreate, user_id: int):
    db_note = models.Note(**note.dict(), owner_id=user_id)
    db.add(db_note)
    db.commit()
    db.refresh(db_note)

    return db_note


def update_note(db: Session, user_id: int, note_id: int, to_change: Dict[str, str]):
    to_change = {key: value for key, value in to_change.items() if value}

    if to_change:
        updated_note = db.query(models.Note).\
            filter(models.Note.id == note_id, models.Note.owner_id == user_id).\
            update(to_change, synchronize_session="fetch")

        db.commit()

    return updated_note


def delete_note(db: Session, note_id: int, user_id: int):
    deleted_note = db.query(models.Note).\
        filter(models.Note.id == note_id,
               models.Note.owner_id == user_id).\
        delete(synchronize_session="fetch")

    db.commit()

    return deleted_note
