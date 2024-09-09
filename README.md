# Car Management Application

Это веб-приложение для управления информацией об автомобилях, разработанное с использованием Django и Django REST Framework.

## Требования

- Docker
- Docker Compose

## Установка и запуск

1. Клонируйте репозиторий:

```bash
git clone https://github.com/SergeyGr07/car_management_django_app
cd car_management_django_app
```

2. Создайте файл .env в корневой директории проекта и заполните его следующим содержимым:

```.env
DEBUG=0
SECRET_KEY=your_secret_key_here
DJANGO_ALLOWED_HOSTS=localhost 127.0.0.1 [::1]
CSRF_TRUSTED_ORIGINS=http://localhost:1337 http://127.0.0.1:1337
SQL_ENGINE=django.db.backends.postgresql
SQL_DATABASE=car_management
SQL_USER=car_management_user
SQL_PASSWORD=your_strong_password
SQL_HOST=db
SQL_PORT=5432
DATABASE=postgres
```

3. Создайте файл .env.db в корневой директории проекта и заполните его следующим содержимым:

```.env
POSTGRES_USER=car_management_user
POSTGRES_PASSWORD=your_strong_password
POSTGRES_DB=car_management
```

4. Соберите и запустите контейнеры:

```bash
docker compose up --build -d
```

5. Примените миграции:

```bash
docker compose exec web python manage.py migrate
```

6. Создайте суперпользователя:

```bash
docker compose exec web python manage.py createsuperuser
```

Приложение будет доступно по адресу `http://localhost:1337`

## Разработка

Для запуска сервера разработки:

1. Остановите production контейнеры:

```bash
docker compose down
```

2. Измените значение DEBUG на 1 в файле .env:

```.env
DEBUG=1
```

3. Запустите контейнеры в режиме разработки:

```bash
docker compose up
```

Сервер разработки будет доступен по адресу `http://localhost:1337`

## Миграции базы данных

Для создания новых миграций:

```bash
docker compose exec web python manage.py makemigrations
```

Для применения миграций:

```bash
docker compose exec web python manage.py migrate
```

## API

API доступно по следующим конечным точкам:

- GET /api/cars/ - получение списка автомобилей
- GET /api/cars/<id>/ - получение информации о конкретном автомобиле
- POST /api/cars/ - создание нового автомобиля
- PUT /api/cars/<id>/ - обновление информации о автомобиле
- DELETE /api/cars/<id>/ - удаление автомобиля
- GET /api/cars/<id>/comments/ - получение комментариев к автомобилю
- POST /api/cars/<id>/comments/ - добавление нового комментария к автомобилю

Для использования API необходимо быть аутентифицированным пользователем.

Пример запроса для получения списка автомобилей:

```bash
curl -H "Authorization: Token YOUR_TOKEN_HERE" `http://localhost:1337/api/cars/`
```
