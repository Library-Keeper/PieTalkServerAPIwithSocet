from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

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


@app.post('/users/')
def create_account(account: schemas.AccountCreate, db: Session = Depends(get_db)):
    db_account = crud.getUserByEmail(db, email=account.email)
    if db_account:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.createAccount(db, account=account)


@app.get("/users/")
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.getUsers(db, skip=skip, limit=limit)
    return users





















