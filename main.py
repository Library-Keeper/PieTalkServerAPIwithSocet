import os
import sqlite3
from fastapi import FastAPI, WebSocket


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


'''
Подключение к БД и её создания в случает отсутствия.
Плюс создание курсора для взаимодействия
'''

connectionSQL = sqlite3.connect('PieTalkDB_MAIN.db')
cursor = connectionSQL.cursor()


cursor.execute('''
CREATE TABLE IF NOT EXISTS Users (
id VARCHAR(127) PRIMARY KEY,
login TEXT NOT NULL UNIQUE,
username TEXT NOT NULL,
email TEXT NOT NULL UNIQUE,
age INTEGER,
description VARCHAR(1023),
status SMALLINT
)
''')


cursor.execute('''
CREATE TABLE IF NOT EXISTS Accounts (
id VARCHAR(127) PRIMARY KEY,
login TEXT UNIQUE,
password TEXT NOT NULL,
email TEXT NOT NULL UNIQUE
)
''')


cursor.execute('''
CREATE TABLE IF NOT EXISTS Messages (
msg_id VARCHAR(127) PRIMARY KEY,
from_id TEXT NOT NULL UNIQUE,
to_id TEXT NOT NULL UNIQUE,
message TEXT NOT NULL
)
''')


connectionSQL.commit()


connectionSQL.close()