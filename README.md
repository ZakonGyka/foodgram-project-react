# Дипломный проект Foodgram

# ![Foodgram_workflow](https://github.com/zakongyka/foodgram-project-react/actions/workflows/Foodgram_workflow.yml/badge.svg)

## Адрес

- http://hamster.sytes.net

## Описание

Проект Foodgram это — «Продуктовый помощник». На этом сервисе пользователи могут публиковать рецепты, подписываться на публикации других пользователей, добавлять понравившиеся рецепты в список «Избранное», а перед походом в магазин скачивать сводный список продуктов, необходимых для приготовления одного или нескольких выбранных блюд.

 ## Установка

- Склонируйте репозиторий
- В файле docker-compose.yaml заменить в объектах backend и frontend - image на build для создания локального образа
- - Запустить сборку проекта:
```Python
docker-compose up
```
- Проверить, что проект запустился
- Создать образ проекта: 
```Python
docker build -t <логин dockerhub>/<имя проекта> .
```
- Проверить, что:
    - образ проекта создается
    - контейнеры создается
- Отправьте созданные образы backend и frontend на docker.hub
- Заменить файле docker-compose.yaml build на image для использования образов с репозитория docker.hub
- Создать файл .env  в директории infra/, указать следующие переменные:
  - DB_ENGINE=django.db.backends.postgresql # используемая база данных - PostgreSQL
  - DB_NAME=postgres # имя базы данных
  - POSTGRES_USER=postgres # логин для подключения к базе данных
  - POSTGRES_PASSWORD=postgres # пароль для подключения к базе данных (установите свой)
  - DB_HOST=db # название сервиса (контейнера)
  - DB_PORT=5432 # порт для подключения к базе данных
- Настроить сервер (пример Linux/Ubunta):
  - обновите индекс пакетов: $ sudo apt update 
  - установите обновления: $ sudo apt upgrade -y
  - установите python, venv, git: $ sudo apt install python3-pip python3-venv git -y
  - Копируйте файл docker-compose.yaml на сервер
  - Копируйте файл nginx.conf на сервер
- Запустите docker-compose up
- Создайте учетную запись администратора: $ sudo docker-compose exec web python manage.py createsuperuser
- Миграции и сбор статики произврдится автоматически при сборке проекта

В приложения настроено Continuous Integration и Continuous Deployment:
- автоматический запуск тестов,
- обновление образов на Docker Hub,
- автоматический деплой на боевой сервер при пуше в главную ветку main.

## Приложение в качестве CI/CD использует GitActions:
- Тестирование по PEP8
- Обновление образов на DockerHub
- Автоматической деплой нового образа на беовой сервер

## Стек технологий

- Python==3.7
- Django==3.2
- djangorestframework==3.13.1
- djoser==2.1.0
- flake8==4.0.1
- Pillow==9.0.1
- psycopg2-binary==2.8.6
- PyJWT==2.3.0
- reportlab==3.6.11
- gunicorn==20.0.4

## Авторы

- https://github.com/ZakonGyka

MIT License

Copyright (c) [2022] [Zakon_Gyka]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
