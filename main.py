from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
from typing import List

import crud, models, schemas
from database import SessionLocal, engine

'''
PieTalkServerAPIwithSocket - серверная часть мессенджера для курсовой работы
Будет реализованна структура API и WebSocket для корректного взаимодействия с
клиентом.

Клиентская часть дла Android будет написана на Kotlin и возможно с примесью Java
Клиентская часть дла Windows будет написана на Python использую скорее всего PyQt5

В Данном проекте будет 1 БД(база данных). А в ней уже 3 таблицы:
1) Users - общая информация о пользователе, все что здесь указанно будет в открытом 
    доступе (кроме email)
2) Accounts - таблица которая будет хранить логин и пароль(хеш) от аккаунта. 
    Информация с этой таблицы будет в закрытом доступе. И возможно с шифрованием.
3) Messages - таблица со всеми сообщениями. Доступ можно будет получить только к
    сообщениям в который указан id вашего аккаунта
'''


models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# Зависимость
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post('/msg/create/', name="Message create")
def createMessage(message: schemas.MessagesCreate, db: Session = Depends(get_db)):
    return crud.createMessage(db, message=message)


@app.post('/user/create/', name="Account create")
def createAccount(account: schemas.AccountCreate, db: Session = Depends(get_db)):
    db_account = crud.getUserByEmail(db, email=account.email)
    if db_account:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.createAccount(db, account=account)


@app.get("/users/", name="Get user list")
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.getUsers(db, skip=skip, limit=limit)
    return users


@app.get("/user/id/{uid}", name="Get user by ID")
def searchUserByID(uid: int, db: Session = Depends(get_db)):
    user = crud.getUserByID(db, user_id=uid)
    return user


@app.get("/user/username/{username}", name="Get user by username")
def searchUserByUsername(username: str, db: Session = Depends(get_db)):
    user = crud.getUserByUsername(db, username=username)
    return user


@app.post("/user/change/username/", name="Change username")
def changeUsername(user_id: int, username: str, db: Session = Depends(get_db)):
    user = crud.changeUsernameByUserID(db,user_id=user_id, username=username)
    return user



















