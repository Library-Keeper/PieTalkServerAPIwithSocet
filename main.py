from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from passlib.hash import pbkdf2_sha512

from fastapi import FastAPI, Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

import crud, models, schemas, uuid
from database import SessionLocal, engine

'''
PieTalkServerAPIwithSocket - серверная часть мессенджера для курсовой работы
Будет реализованна структура API и WebSocket для корректного взаимодействия с
клиентом.

Клиентская часть дла Android будет написана на Kotlin и возможно с примесью Java
Клиентская часть дла Windows будет написана на Python использую скорее всего PyQt5

В Данном проекте будет 1 БД(база данных). А в ней уже 5 таблиц:
1) Users - общая информация о пользователе, все что здесь указанно будет в открытом 
    доступе (кроме email)
2) Messages - таблица со всеми сообщениями. Доступ можно будет получить только к
    сообщениям в который указан id вашего аккаунта
3) Groups - таблица для с информацией о чата/группах
4) GroupMembers - таблица с информацией в каких чата/группах участвует пользователь
5) Attachments* - Таблица с вложениями к сообщениям от пользователя


* - есть шанс что мне лень и я это не сделаю
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


search = ["email", "id", "login"]


@app.post("/user/create/")
def create_user(email:str, password:str, db: Session = Depends(get_db)):
    """
    Создает аккаунт на основе, пароля и почты\n
    -------\n
    email - почта нового пользователя\n
    password - пароль от нового аккаунта
    """

    db_user = crud.get_user_by_email(db, email=email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db, email, password)


@app.get("/user/search/")
def search_user(search_by: str, search_string: str, db: Session = Depends(get_db)):
    """
    Поиск пользователей по критериям\n
    -------\n
    search_by == "email" -> Возвращает пользователя по почте\n
    search_by == "id" -> Возвращает пользователя по ID\n
    search_by == "login" -> Возвращает пользователя по логину\n
    -------\n
    В иных случаях возвращает ошибку
    """

    if not search_by in search:
        return {"error": "search_by error"}
    if search_by == search[0]:
        return crud.get_user_by_email(db=db, email=search_string)
    if search_by == search[1]:
        return crud.get_user(db=db, user_id=search_string)
    if search_by == search[2]:
        return crud.get_user_by_login(db=db, login=search_string)


@app.post("/user/change/login/")
def change_user_login(user_id: str, login: str, password: str, sessoin: str, db: Session = Depends(get_db)):
    """
    Позволяет изменить пользовательский логин\n
    -------\n
    user_id - id пользователя\n
    login - новый логин\n
    password - пароль от аккаунта\n
    session - код текущей сессии
    """

    return crud.change_user_login(db, user_id, login, password, sessoin)


@app.post("/user/change/username/")
def change_user_username(user_id: str, username: str, sessoin: str, db: Session = Depends(get_db)):
    """
    Позволяет изменить отображаемое имя\n
    -------\n
    user_id - id пользователя\n
    username - новое отображаемое имя\n
    session - код текущей сессии\n
    -------\n
    username менее важен так что дле его изменения не нужен пароль
    """

    return crud.change_user_username(db, user_id, username, sessoin)


@app.post("/user/logout")
def user_logout(user_id: str, session: str, db: Session = Depends(get_db)):

    """
    Выход с аккаунта\n
    При выходе удаляется код сессии и статусу пользователя присваивается 0\n
    -------\n
    user_id - id пользователя\n
    session - код текущей сессии
    """

    return crud.user_logout(db, user_id, session)


@app.post("/user/login")
def user_login(email: str, password: str, db: Session = Depends(get_db)):
    """
    Вход в аккаунт\n
    При входе в конце выдается новый код сессии\n
    и статусу пользователя присваивается 1\n
    -------\n
    email - email пользователя\n
    password - пароль от аккаунта
    """

    return crud.user_login(db, email, password)


@app.post("/msg/send")
def send_msg(from_id: str, to_id: str, content: str, session: str, db: Session = Depends(get_db)):

    """
    Отправка сообщений\n
    Эта функция позволяет отправить сообщение любому пользователю\n
    -------\n
    from_id - id пользователя кто отправляет сообщение\n
    to_id - id пользователя кому отправили сообщение\n
    content - текст самого сообщения\n
    session - код текущей сессии от кого сообщение
    """


    return crud.msg_send(db, from_id, to_id, content, session)


@app.post("/msg/get")
def get_msg(user_id:str, from_id: str, session: str, skip:int = 0, limit:int=100, db: Session = Depends(get_db)):
    """
    Получение списка сообщений\n
    Эта функция позволяет получить список общих с пользователем сосбщений\n
    -------\n
    user_id - id пользователя кто получает список сообщений\n
    from_id - id пользователя из переписки\n
    session - код текущей сессии от кого сообщение\n
    skip - сколько сообщений назад (по умолчанию "0")\n
    limit - количество сообщений за раз (по умолчанию "100")
    """
    return crud.get_msg(db, user_id, from_id, session, skip, limit)

