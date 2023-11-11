import sqlalchemy
from sqlalchemy.orm import Session

from passlib.hash import pbkdf2_sha512

import models
import schemas


def getUsers(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def getUserByID(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def getUserByEmail(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def getUserByUsername(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()


def getUserByLogin(db: Session, user_login: str):
    return db.query(models.User).filter(models.User.login == user_login).first()


def getAccountByID(db: Session, acc_id: int):
    return db.query(models.Account).filter(models.Account.id == acc_id).first()


def getAccountByLogin(db: Session, login: str):
    return db.query(models.Account).filter(models.Account.login == login).first()


def createAccount(db: Session, account: schemas.AccountCreate):
    hashed_password = pbkdf2_sha512.hash(account.password)
    db_account = models.Account(login=account.login, password=hashed_password, email=account.email)
    db_user = models.User(id=db_account.id, login=db_account.login, email=db_account.email, status=0)
    db.add(db_account)
    db.commit()
    db.refresh(db_account)

    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def createMessage(db: Session, message: schemas.MessagesCreate):
    acc = getAccountByID(db, message.from_id)
    if acc.session != message.session:
        return {"detail": "Session error"}
    db_msg = models.Message(from_id=message.from_id, to_id=message.to_id, message=message.message)
    db.add(db_msg)
    db.commit()
    db.refresh(db_msg)
    return db_msg







