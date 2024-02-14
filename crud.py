import sqlalchemy
from sqlalchemy.orm import Session
from sqlalchemy import or_, and_
from datetime import datetime

from passlib.hash import pbkdf2_sha512

from uuid import uuid4
import models
import schemas

e = {"error": "unknown user"}


def get_user(db: Session, user_id: str):
    return db.query(models.User).filter(models.User.user_id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def get_user_by_login(db: Session, login: str):
    return db.query(models.User).filter(models.User.login == login).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def create_user(db: Session, email:str, password:str):
    fake_hashed_password = pbkdf2_sha512.hash(password)
    s = str(uuid4())
    db_user = models.User(
        user_id="u" + str(uuid4()),
        email=email,
        hashed_password=fake_hashed_password,
        session=pbkdf2_sha512.hash(s),
        status=1
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user, s


def change_user_login(db: Session, user_id: str, login: str, password: str, session: str):
    db_user = get_user(db=db, user_id=user_id)
    if not db_user:
        return e
    if not db_user.session:
        return e
    if not pbkdf2_sha512.verify(password, db_user.hashed_password) or not pbkdf2_sha512.verify(session,
                                                                                               db_user.session):
        return e
    db_user.login = login
    db.commit()
    db.refresh(db_user)
    return db_user


def change_user_username(db: Session, user_id: str, username: str, session: str):
    db_user = get_user(db=db, user_id=user_id)
    if not db_user.session:
        return e
    if not db_user or not pbkdf2_sha512.verify(session, db_user.session):
        return e
    db_user.username = username
    db.commit()
    db.refresh(db_user)
    return db_user


def user_logout(db, user_id: str, session: str):
    db_user = get_user(db=db, user_id=user_id)
    if not db_user or not pbkdf2_sha512.verify(session, db_user.session):
        return e
    db_user.session = None
    db_user.status = 0
    db.commit()
    db.refresh(db_user)
    return db_user


def user_login(db, email: str, password: str):
    db_user = get_user_by_email(db=db, email=email)
    if not pbkdf2_sha512.verify(password, db_user.hashed_password) or db_user.session:
        return e
    s = str(uuid4())
    db_user.session = pbkdf2_sha512.hash(s)
    db_user.status = 1
    db.commit()
    db.refresh(db_user)
    return db_user, s


def msg_send(db, from_id: str, to_id: str, content: str, session: str):
    db_from_id = get_user(db=db, user_id=from_id)
    db_to_id = get_user(db=db, user_id=to_id)
    if not db_from_id or not db_to_id:
        return e
    if not db_from_id.session:
        return e
    if not db_from_id or not pbkdf2_sha512.verify(session, db_from_id.session):
        return e

    timestamp = datetime.now()

    db_msg = models.Message(
        from_id=from_id,
        to_id=to_id,
        content=content,
        timestamp=timestamp
    )
    db.add(db_msg)
    db.commit()
    db.refresh(db_msg)
    return db_msg


def get_msg(db, user_id: str, from_id:str, session:str, skip:int = 0, limit:int = 100):
    db_user = get_user(db=db, user_id=user_id)

    if not db_user or not db_user.session:
        return e
    if not pbkdf2_sha512.verify(session, db_user.session):
        return e

    return db.query(models.Message).filter(and_(or_(models.Message.from_id == user_id, models.Message.to_id == user_id),or_(models.Message.from_id == from_id, models.Message.to_id == from_id))).offset(skip).limit(limit).all()


