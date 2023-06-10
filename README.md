# Проект «Учебное развёртывание контейнера» 
![Github actions](https://github.com/snigiden/yamdb_final/actions/workflows/yamdb_workflow.yml/badge.svg)
___
## Используемые технологии:
- Python,
- Django, 
- Django Rest Framework
- Docker
- Telegram bot API
___
## Описание

Данный репозиторий содержит учебный проект по настройке CI/CD для проекта api_yamdb.
___
## Установка и запуск
* Клонировать репозиторий

* Установить docker на удалённый сервер под управлением debian based дистрибутива linux

* Настроить nginx и docker на удалённом сервере

* Создать .env файл

* Отредактировать цепочку секретов

* Повесить бадж прохождения workflow тестов в свой репозиторий

***
## Памятка .env
~~~
DB_ENGINE= СУБД
DB_NAME= имя базы данных
POSTGRES_USER= логин для подключения к базе данных
POSTGRES_PASSWORD= пароль для подключения к БД
DB_HOST= название сервиса (контейнера)
DB_PORT= порт для подключения к БД 
~~~