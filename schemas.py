from typing import Union
from pydantic import BaseModel
from datetime import date


'''
Структуры для создания записей в таблицах
'''


class UserBase(BaseModel):
    pass


class UserCreate(UserBase):
    login: str
    email: str
    username: str = None
    date_birth: Union[date, None] = None
    description: Union[str, None] = None

    class Config:
        orm_mode = True


class UserChange(UserBase):
    id: int
    session: str


class UserChangeUsername(UserChange):
    username: str


class UserChangePassword(UserChange):
    old_pass: str
    new_pass: str


class AccountBase(BaseModel):
    login: str
    password: str


class AccountCreate(AccountBase):
    email: str

    class Config:
        orm_mode = True


class AccountLogout(AccountBase):
    session: str


class MessagesCreate(BaseModel):
    session: str
    from_id: int
    to_id: int
    message: str

    class Config:
        orm_mode = True

