from sqlalchemy import Column, ForeignKey, String, SmallInteger, DATE, Integer
from sqlalchemy.orm import relationship
from database import Base

'''
Таблица Users
id          - уникальный текстовый идентификатор (по типу "library_keeper", "nasya_velikaya2008" и т.д.)
login       - уникальный логин для входа в аккаунт
username    - пользовательское имя/псевдоним
email       - привязанная к аккаунту электронная почта
date_birth  - установленный пользователем дата рождения
description - установленное пользователем описание
status      - состояние пользователя (онлайн, оффлайн, не беспокоить и т.д.)
'''


class User(Base):
    __tablename__ = "Users"

    id = Column(Integer, primary_key=True, index=True)
    login = Column(String, unique=True, index=True)
    username = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    date_birth = Column(DATE)
    description = Column(String)
    status = Column(SmallInteger)


'''
Таблица Accounts
id        - уникальный текстовый идентификатор (по типу "library_keeper", "nasya_velikaya2008" и т.д.)
login     - уникальный логин для входа в аккаунт
password  - пароль пользователя в Хеш формате для большей безопасности
email     - электронная почта для привязки к аккаунту
'''


class Account(Base):
    __tablename__ = "Accounts"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    login = Column(String, unique=True, index=True)
    password = Column(String)
    email = Column(String, unique=True, index=True)


'''
Таблица Messages
msg_id   - уникальный идентификационный номер сообщения
from_id  - текстовый идентификатор отправителя
to_id    - текстовый идентификатор получателя
message  - отправленное сообщение
'''


class Message(Base):
    __tablename__ = "Messages"

    msg_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    from_id = Column(Integer)
    to_id = Column(Integer)
    message = Column(String)
