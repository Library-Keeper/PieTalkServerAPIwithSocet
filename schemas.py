from typing import Union
from pydantic import BaseModel
from datetime import date


class UserBase(BaseModel):
    pass


class UserCreate(UserBase):
    login: str
    username: str = None
    email: str
    date_birth: Union[date, None] = None
    description: Union[str, None] = None

    class Config:
        orm_mode = True


class AccountBase(BaseModel):
    pass


class AccountCreate(AccountBase):
    login: str
    email: str
    password: str

    class Config:
        orm_mode = True


class MessagesBase(BaseModel):
    pass


class MessagesCreate(MessagesBase):

    from_id: int
    to_id: int
    message: str

    class Config:
        orm_mode = True


