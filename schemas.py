from typing import Union
from pydantic import BaseModel
from sqlalchemy import Date
import datetime

'''
Структуры для создания записей в таблицах
'''


class UserBase(BaseModel):
    email: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: str
    login: str
    username: str
    date_birth: datetime.date
    description: str
    stats: str

    class Config:
        orm_mode = True


class MessageBase(BaseModel):
    content: str
    from_id: str
    to_id: str


class MessageCreate(MessageBase):
    session: str


class Message(MessageBase):
    msg_id: int
    timestamp: datetime.datetime

    class Config:
        orm_mode = True


class GroupCreate(BaseModel):
    group_name: str


class Group(GroupCreate):
    group_id: str
    owner_id: str
    created_at: datetime.datetime


class GroupJoin(BaseModel):
    group_id: str
    user_id: str