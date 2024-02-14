from sqlalchemy import Column, ForeignKey, String, SmallInteger, Date, Integer, DateTime, Boolean
from sqlalchemy.orm import relationship
from database import Base

from typing import Union

'''
Таблица User
user_id       - уникальный текстовый ID (по типу "library_keeper", "nasya_velikaya2008" и т.д.)
login         - уникальный логин для входа в аккаунт
username      - пользовательское имя/псевдоним
email         - привязанная к аккаунту электронная почта
date_birth    - установленный пользователем дата рождения
description   - установленное пользователем описание
status        - состояние пользователя (онлайн, оффлайн, не беспокоить и т.д.)
hashed_password - хеш пароля для безопасности
'''


class User(Base):
    __tablename__ = "User"

    user_id = Column(String, primary_key=True)
    login = Column(String, unique=True, index=True)
    username = Column(String)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    session = Column(String)
    date_birth = Column(Date)
    description = Column(String)
    status = Column(SmallInteger)


'''
Таблица Messages
msg_id    - уникальный ID номер сообщения
from_id   - текстовый ID отправителя (из User)
to_id     - текстовый ID получателя (из User/Groups)
content   - отправленное сообщение
timestamp - время отправления
'''


class Message(Base):
    __tablename__ = "Messages"

    msg_id = Column(Integer, primary_key=True, autoincrement=True)
    from_id = Column(String, ForeignKey("User.user_id"))
    to_id = Column(String)
    content = Column(String)
    timestamp = Column(DateTime)


'''
Таблица Group
group_id    - уникальный ID чата/группы
group_name  - имя чата/группы
owner_id    - ID пользователя или владельца группы (из User)
created_at  - дата начала беседы или создания группы
'''


class Group(Base):
    __tablename__ = "Group"

    group_id = Column(String, primary_key=True)
    group_name = Column(String)
    owner_id = Column(String, ForeignKey("User.user_id"))
    created_at = Column(DateTime)


'''
Таблица GroupMembers
group_id  - ID чата/группы (из User/Groups)
user_id   - ID пользователя (из User)
'''


class GroupMember(Base):
    __tablename__ = "GroupMember"

    id = Column(Integer, autoincrement=True, primary_key=True)
    group_id = Column(String)
    user_id = Column(String, ForeignKey("User.user_id"))



