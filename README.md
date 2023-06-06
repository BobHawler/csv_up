# CSV_UP

Сервис позволяет создавать пользователя и загружать csv файлы произвольного содержания и получать из них данные с возможностью фильтрации и сортировки.

## В сервисе реализованы следующие эндпоинты:
- /registration (POST)
- /upload (POST)
- /files (GET)
- /data (GET)

## Скачивание проекта и подготовка файлов:

### Создайте папку:
```bash
mkdir csv_up
```

### Перейдите в папку:
```bash
cd csv_up
```
### Скачайте репозиторий:
```bash
git clone git@github.com:BobHawler/csv_up.git
```

### Перейдите в папку проекта:
```bash
cd csv_up
```

### Создйте .env файл:
```bash
touch .env
```

### В .env файле укажите данные своей базы данных.
Пример наполнения можно увидеть в файле .env_example:
```bash
POSTGRES_DB=questions_db
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
```

## Создание и запуск контейнера:

### Сборка образов и запуск котейнеров:

```bash
docker-compose up -d --build
```
### Остановка контейнеров:
```bash
docker-compose stop
```
### Повторный запуск контейнеров:
```bash
docker-compose up
```
Данные БД хранятся в volumes

## Инициализация БД (выполняется внутри контейнера):
```bash
docker-compose exec app bash
```
```bash
flask db init
flask db migrate
flask db upgrade
```

## Примеры запросов:

### Запрос на создание пользователя:
curl -i -H "Content-Type:application/json; charset=utf-8" -X POST --data '{"username":"admin", "password":"admin"}' http://localhost:5000/registration

### Запрос для загрузки фала:
curl -u admin:admin -X POST -F "file=@IT.csv" http://localhost:5000/upload

### Получение списка файлов с информацией о колонках:
curl -u admin:admin http://localhost:5000/files

### Запрос на получение данных из конкретного файла с опциональной фильтрацией и сортировкой по одному или нескольким столбцам:
curl -u admin:admin "http://localhost:5000/data?filename=IT.csv&filter_col=Brand"

## В проекте предусмотрен файл с тестами - test.py

### Запуск тестов:
```
python -m unittest test.py
```

## Автор:
Анатолий Коновалов (BobHawler)
