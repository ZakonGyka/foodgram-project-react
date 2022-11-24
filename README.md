# Дипломный проект Foodgram

# ![Foodgram_workflow](https://github.com/zakongyka/foodgram-project-react/actions/workflows/Foodgram_workflow.yml/badge.svg)

## Адрес

- http://hamster.sytes.net

## Описание

Проект Foodgram это — «Продуктовый помощник». На этом сервисе пользователи могут публиковать рецепты, подписываться на публикации других пользователей, добавлять понравившиеся рецепты в список «Избранное», а перед походом в магазин скачивать сводный список продуктов, необходимых для приготовления одного или нескольких выбранных блюд.

 ## Установка
 ### Локальное тестирование
- Склонируйте репозиторий

- В foodgram-project-react/backend/backend/settings.py в ALLOWED_HOSTS добавьте '*' - для доступа ко всем IP.
- В foodgram-project-react/backend/backend/settings.py раскомментируйте DATABASES ("""for local testing""")
- В foodgram-project-react/backend/backend/settings.py закомментируйте DATABASES (где используется os.getenv)

- В nginx.conf раскомментируйте proxy_pass http://host.docker.internal:8000/api/; - for local testing ("- for local testing" удалить)
- В nginx.conf раскомментируйте proxy_pass http://host.docker.internal:8000/admin/; - for local testing ("- for local testing" удалить)
- В nginx.conf закомментируйте proxy_pass http://backend:8000/api/;
- В nginx.conf закомментируйте proxy_pass http://backend:8000/admin/;

- В файле docker-compose.yaml заменить в объекте backend - закомментируйте строчку с image, добавьте build для создания локального образа:
```Python
    build:
      context: ../backend
      dockerfile: Dockerfile
    image: zakongyka/backend:latest 
```
- В файле docker-compose.yaml заменить в объекте frontend - закомментируйте строчку с image, добавьте build для создания локального образа:
```Python
    build:
      context: ../frontend
      dockerfile: Dockerfile
    image: zakongyka/frontend:v1
```

- Запустите сборку проекта:
```Python
docker-compose up
```

- Запустится 3 контейнера, оставноите конейтнер backend, оставь работать контейнеры postgre и nginx

- Запустите локальный сервер:
```Python
python manage.py runserver
```

- Миграции и сбор статики произврдится автоматически при сборке проекта!

- Создайте superuser:
```Python
python manage.py createsuperuser
```

- Проверить, что проект запустился локально, перейдите на сервер по своему локальному IP
- Найстройте в IDE DEBUG на запуск локального сервера (python manage.py runserver)

### Подготовка к боевому развертыванию:

- Создайте два образа: backend и frontend
```Python
docker build -t <логин dockerhub>/<имя проекта> .
```

- Отправьте созданные образы backend и frontend на docker.hub

- Заменить файле docker-compose.yaml build на image для использования образов с репозитория docker.hub (те строки что была закомментированы в начале)

- В foodgram-project-react/backend/backend/settings.py закомментируйте DATABASES ("""for local testing""")
- В foodgram-project-react/backend/backend/settings.py закомментируйте DATABASES (где используется os.getenv)

- Создать файл .env в директории infra/, указать следующие переменные:
  - DB_ENGINE=django.db.backends.postgresql # используемая база данных - PostgreSQL
  - DB_NAME=postgres # имя базы данных
  - POSTGRES_USER=postgres # логин для подключения к базе данных
  - POSTGRES_PASSWORD=postgres # пароль для подключения к базе данных (установите свой)
  - DB_HOST=db # название сервиса (контейнера)
  - DB_PORT=5432 # порт для подключения к базе данных
  
- В nginx.conf закомментируйте proxy_pass http://host.docker.internal:8000/api/; - for local testing ("- for local testing" удалить)
- В nginx.conf закомментируйте proxy_pass http://host.docker.internal:8000/admin/; - for local testing ("- for local testing" удалить)
- В nginx.conf раскомментируйте proxy_pass http://backend:8000/api/;
- В nginx.conf раскомментируйте proxy_pass http://backend:8000/admin/;

- Запустите сборку проекта:
```Python
docker-compose up
```

- Весь проект должен был заработать из конейтенеров.

- Настроить сервер (пример Linux/Ubunta):
  - обновите индекс пакетов: $ sudo apt update 
  - установите обновления: $ sudo apt upgrade -y
  - установите python, venv, git: $ sudo apt install python3-pip python3-venv git -y
  - Копируйте файл docker-compose.yaml на сервер
  - Копируйте файл nginx.conf на сервер
  
- Запустите на сервере docker-compose up

- Миграции и сбор статики произврдится автоматически при сборке проекта!

- Войдите в контейнер backend и создайте учетную запись администратора:
```Python
sudo docker exec -it <ID backend контейнера> bash
python manage.py createsuperuser
```
### В приложения настроено Continuous Integration и Continuous Deployment:
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
