# Дипломный проект Foodgram

# ![Foodgram_workflow](https://github.com/zakongyka/foodgram-project-react/actions/workflows/Foodgram_workflow.yml/badge.svg)

## Адрес

http://hamster.sytes.net


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
- тестирование по PEP8
- Обновление образов на DockerHub
- Автоматической деплой нового образа на беовой сервер

## Стек технологий

- asgiref==3.5.0
- autopep8==1.6.0
- certifi==2021.10.8
- cffi==1.15.0
- charset-normalizer==2.0.12
- coreapi==2.3.3
- coreschema==0.0.4
- cryptography==36.0.1
- defusedxml==0.7.1
- Django==2.2.19
- django-colorfield==0.6.3
- django-extra-fields==3.0.2
- django-filter==21.1
- django-rest-framework==0.1.0
- django-templated-mail==1.1.1
- djangorestframework==3.13.1
- djoser==2.1.0
- flake8==4.0.1
- idna==3.3
- importlib-metadata==1.7.0
- itypes==1.2.0
- Jinja2==3.0.3
- MarkupSafe==2.1.0
- mccabe==0.6.1
- oauthlib==3.2.0
- Pillow==9.0.1
- psycopg2-binary==2.8.6
- pycodestyle==2.8.0
- pycparser==2.21
- pyflakes==2.4.0
- PyJWT==2.3.0
- python-dotenv==0.19.2
- python3-openid==3.2.0
- pytz==2021.3
- reportlab==3.6.9
- requests==2.27.1
- requests-oauthlib==1.3.1
- six==1.16.0
- social-auth-app-django==4.0.0
- social-auth-core==4.2.0
- sqlparse==0.4.2
- toml==0.10.2
- typing_extensions==4.1.1
- uritemplate==4.1.1
- urllib3==1.26.8
- zipp==3.7.0
- gunicorn==20.0.4


## Примеры

Примеры запросов по API:

- [GET] /api/users/ - Получить список всех пользователей.
- [POST] /api/users/ - Регистрация пользователя.
- [GET] /api/tags/ - Получить список всех тегов.
- [POST] /api/recipes/ - Создание рецепта.
- [GET] /api/recipes/download_shopping_cart/ - Скачать файл со списком покупок.
- [POST] /api/recipes/{id}/favorite/ - Добавить рецепт в избранное.
- [DEL] /api/users/{id}/subscribe/ - Отписаться от пользователя.
- [GET] /api/ingredients/ - Список ингредиентов с возможностью поиска по имени.


## Авторы

Рустам Вахитов
